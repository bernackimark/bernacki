import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# anvil notes: outcome was an enum but no support, no return type pipe operator allowed
import random
from datetime import datetime
from .. import games_module as gm


class UI:
    instructions_text = '''For each game, a secret color sequence is generated, and your goal is to guess sequence before you are out of chances.
    
                        Once you have started the game, you will see a list of available colors to choose from.  The secret color sequence will be comprised of those colors -- each color can be used zero, once, or multiple times.  Click on an available color to add it to your guess.  Once you've added a color to your guess, you can click on it again to remove it from your guess.  Once you are happy with your guess, click on the submit button.
                        
                        Each of your guesses will be shown in Your Previous Guess section at the bottom.  The 'Correct #' will tell you how many colors you got in the correct position.  The 'Incorrect #' will tell you how many colors you have correctly identified but in the incorrect position. 
                        
                        If you want to increase or decrease the difficulty, when starting a new game, you can adjust the available colors, the length of the secret sequence, and the number of guesses you are allowed.
                        
                        Happy Masterminding.  Love, Bernacki'''
  
    prompt_datatype_answers = [
        {'prompt': 'How many possible colors would you like to choose from (4 to 6)?', 'datatype': 'int', 'answers': [4, 5, 6]},
        {'prompt': 'How long of a sequence would you like (between 1 and 6)?', 'datatype': 'int', 'answers': [1, 2, 3, 4, 5, 6]},
        {'prompt': 'How many guesses would you like to allow yourself (between 1 and 20)?', 'datatype': 'int', 'answers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}
    ]

class Color:
    def __init__(self, color: str, image: str):
        self.color = color
        self.image = image

    def __repr__(self):
        return self.color


class ColorBank:
    def __init__(self, color_set_cnt: int):
        all_colors = ['r', 'y', 'g', 'c', 'b', 'p']
        self.game_color_objects = [Color(c, f'_/theme/mastermind/mm_{c}.png') for idx, c in enumerate(all_colors) if idx + 1 <= color_set_cnt]
    def __repr__(self):
        return ' '.join([c.color for c in self.game_color_objects])

    @property
    def game_color_list(self):
        return [c.color for c in self.game_color_objects]

    def get_color_from_letter(self, letter: str) -> Color:
        return [c for c in self.game_color_objects if letter == c.color][0]


class Guess:
    def __init__(self):
        self.color_objects = []

    @property
    def guess_str(self):
        return [c.color for c in self.color_objects]

    @property
    def guess_len(self):
        return len(self.color_objects)

    def add_guess_str(self, color_str: str) -> bool:
        if len(self.color_objects) >= mastermind.answer_len:
            return False
        self.color_objects.append(mastermind.color_bank.get_color_from_letter(color_str))
        return True

    def add_guess_object(self, color: Color):
        if len(self.color_objects) >= mastermind.answer_len:
            print('No more guesses remaining')
            return
        self.color_objects.append(color)

    def remove_guess_object(self, idx):
        self.color_objects.pop(idx)

    def clear_my_guess(self):
        self.color_objects.clear()


class Mastermind(gm.Game):
    def __init__(self, player_emails: list[str], color_set_cnt: int, answer_len: int, max_guess_cnt: int):
        super().__init__('mastermind', player_emails)
        self.color_set_cnt = color_set_cnt
        self.color_bank = ColorBank(color_set_cnt)
        self.answer_len = answer_len
        self.generated_answer = [random.choice(self.color_bank.game_color_objects) for _ in range(self.answer_len)]
        self.max_guess_cnt = max_guess_cnt
        self.guess_number = 0
        self.round_list = []
        self.outcome = 'no_result'
        self.state = 'guessing'

    @property
    def as_dictionary(self) -> dict:
        return self.__dict__

    @property
    def game_data_dict(self) -> dict:
        return {'color_set_cnt': self.color_set_cnt, 'answer_len': self.answer_len, 'max_guess_cnt': self.max_guess_cnt,
                'guesses_used': self.guess_number, 'outcome': self.outcome}
  
    @property
    def answer_str(self):
        return [c.color for c in self.generated_answer]

    def increment_guess_cnt(self):
        self.guess_number += 1

    def evaluate_answer_log_result(self):
        self.increment_guess_cnt()
        round_result: dict = compare_guess_to_answer()
        self.round_list.append(round_result)

    @property
    def is_winner(self) -> bool:
        return self.round_list[-1]['correct_pos_cnt'] == self.answer_len

    def check_for_end_game(self):
        if self.is_winner:
            self.outcome = 'win'
            self.state = 'game_over'
            self.send_end_game_data_to_parent()
            self.write_game_to_db()
            return
        if self.guess_number == self.max_guess_cnt:
            self.outcome = 'loss'
            self.state = 'game_over'
            self.send_end_game_data_to_parent()
            self.write_game_to_db()
            return

    def send_end_game_data_to_parent(self):
        self.game_data = self.game_data_dict


def compare_guess_to_answer() -> dict:
    correct_pos_cnt, total_correct_cnt = 0, 0
    answer_copy = mastermind.answer_str.copy()

    for c in guess.guess_str:
        if c in answer_copy:
            answer_copy.remove(c)
            total_correct_cnt += 1
    for i in range(mastermind.answer_len):
        if guess.guess_str[i] == mastermind.answer_str[i]:
            correct_pos_cnt += 1
    incorrect_pos_cnt = total_correct_cnt - correct_pos_cnt
    return {'guess_number': mastermind.guess_number, 'guess': guess.color_objects.copy(),
            'correct_pos_cnt': correct_pos_cnt, 'incorrect_pos_cnt': incorrect_pos_cnt}


def is_guess_full() -> bool:
    print(mastermind.answer_len, guess.guess_len)
    return mastermind.answer_len == guess.guess_len


mastermind: Mastermind
guess = Guess()

# after knowing all of the letters, regardless of position:
# 4 of same letter = 1 permutation
# 3 of same letter, 1 = 4 permutations
# 2 of same letter, 2 of same letter = 6 permutations
# 2 of same letter, 1, 1 = 12 permutations
#   if 2 correct & 2 incorrect:
#       6 perms left
#   if 1 correct & 3 incorrect:
#       4 perms left
# all different letters = 24 permutations
#   if 2 correct & 2 incorrect:
#       9 perms left
#           0 x3, 1 x3, 2 x2, 3 x0, 4 x1

# come up with a bot to solve this

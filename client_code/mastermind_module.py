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


class UI:
    prompt_datatype_answers = [
        {'prompt': 'How many possible colors would you like to choose from (4 to 6)?', 'datatype': 'int', 'answers': [4, 5, 6]},
        {'prompt': 'How long of a sequence would you like (between 1 and 10)?', 'datatype': 'int', 'answers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        {'prompt': 'How many guesses would you like to allow yourself (between 1 and 20)?', 'datatype': 'int', 'answers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}
    ]

    @staticmethod
    def get_user_input(prompt_datatype_answer: dict):  # return type is int | str ... no anvil support for this
        print(prompt_datatype_answer['prompt'])
        cnt = 0
        while cnt not in prompt_datatype_answer['answers']:
            if prompt_datatype_answer['datatype'] == 'int':
                cnt = int(input())
            else:
                cnt = input()
        return cnt

    @staticmethod
    def get_user_guess() -> list:
        print(f'Please guess {game.answer_len} colors. ')
        return [input() for _ in range(game.answer_len)]

    @staticmethod
    def display_answer() -> None:
        answer = [c.color for c in game.generated_answer]
        print(f'The answer is {answer}')

    @staticmethod
    def display_color_set() -> None:
        print(f'Your color options are {color_bank.game_color_list}')

    @staticmethod
    def display_guess_result() -> None:
        print(f'Guess #{game.guess_cnt} of {game.max_guess_cnt}. {round.guess} has {round.correct_pos_cnt} correct positions & {round.incorrect_pos_cnt} incorrect positions.')

    @staticmethod
    def display_game_result() -> None:
        print(f'{game.result_dict}')


class Color:
    def __init__(self, color: str, image: str):
        self.color = color
        self.image = image


class ColorBank:
    def __init__(self, color_set_cnt: int):
        all_colors = ['r', 'y', 'g', 'c', 'b', 'p']
        self.game_color_objects = [Color(c, f'_/theme/mastermind/mm_{c}.png') for idx, c in enumerate(all_colors) if idx + 1 <= color_set_cnt]
  
    @property
    def game_color_list(self):
        return [c.color for c in self.game_color_objects]

    def get_color_from_letter(self, letter: str) -> Color:
        return [c for c in self.game_color_objects if letter == c.color][0]


# should there be a parent Game class that creates the shell for all games?
# email, app_name, start, end, ?maybe outcome?
class Game:
    def __init__(self, email: str, max_guess_cnt, color_set_cnt, answer_len):
        self.user_email = email
        self.app_name = 'mastermind'
        self.start_time = datetime.utcnow()
        self.end_time = ''
        self.color_set_cnt = color_set_cnt
        self.answer_len = answer_len
        self.generated_answer = []  # will be a list[Color]
        self.max_guess_cnt = max_guess_cnt
        self.guess_cnt = 0
        self.round_list = []
        self.outcome = 'no_result'

    @property
    def answer_str(self):
        return [c.color for c in self.generated_answer]

    def generate_answer(self):
        self.generated_answer = [random.choice(color_bank.game_color_objects) for _ in range(self.answer_len)]

    def update_round_list(self, round_obj):
        self.round_list.append(round_obj)

    def increment_guess_cnt(self):
        self.guess_cnt += 1

    def update_outcome(self, outcome: str):
        self.outcome = outcome

    @property
    def result_dict(self):
        return {'email': self.user_email, 'app': self.app_name,
                'start_time': self.start_time, 'end_time': datetime.utcnow(),
                'color_set_cnt': self.color_set_cnt, 'answer': self.answer_str, 'answer_len': self.answer_len,
                'max_guess_cnt': self.max_guess_cnt, 'actual_guess_cnt': self.guess_cnt,
                'correct_pos_cnt': round.correct_pos_cnt, 'incorrect_pos_cnt': round.incorrect_pos_cnt,
                'outcome': self.outcome}


class Round:
    def __init__(self):
        self.guess_cnt = game.guess_cnt
        self.guess = []  # this is a list[Color]
        self.correct_pos_cnt = 0
        self.incorrect_pos_cnt = 0

    # since i'm just dumping the entire object into a dictionary, not sure this is necessary
    @property
    def guess_result(self) -> dict:
        return {'guess_cnt': self.guess_cnt, 'guess': self.guess,
                'correct_pos_cnt': self.correct_pos_cnt, 'incorrect_pos_cnt': self.incorrect_pos_cnt}

    def compare_answer_and_guess(self) -> None:
        total_correct_cnt = 0
        answer_copy = game.answer_str.copy()
        for c in self.guess:
            if c in answer_copy:
                answer_copy.remove(c)
                total_correct_cnt += 1
        for i in range(game.answer_len):
            if self.guess[i] == game.answer_str[i]:
                self.correct_pos_cnt += 1
        self.incorrect_pos_cnt = total_correct_cnt - self.correct_pos_cnt


def create_new_game(email, color_set_cnt, answer_len, max_guess_cnt):
    global color_bank
    color_bank = ColorBank(color_set_cnt)
    print(f'Color Bank is: {color_bank.game_color_list}')
    global game
    game = Game(email=email, max_guess_cnt=max_guess_cnt, color_set_cnt=color_set_cnt, answer_len=answer_len)
    game.generate_answer()
    # UI.display_answer()
    UI.display_color_set()
    

    # while True:
    #     game.increment_guess_cnt()
    #     round = Round()
    #     # guess = UI.get_user_guess()  # anvil_remove
    #     round.guess = guess
    #     round.compare_answer_and_guess()
    #     game.update_round_list(round.guess_result)
    #     UI.display_guess_result()
    #     if round.correct_pos_cnt == game.answer_len:
    #         game.update_outcome('win')
    #         UI.display_game_result()
    #         break
    #     if round.guess_cnt == game.max_guess_cnt:
    #         game.update_outcome('loss')
    #         UI.display_game_result()
    #         break


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

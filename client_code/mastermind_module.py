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
        {'prompt': 'How long of a sequence would you like (between 1 and 6)?', 'datatype': 'int', 'answers': [1, 2, 3, 4, 5, 6]},
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
        print(f'Guess #{game.guess_cnt} of {game.max_guess_cnt}. {round_.guess} has {round_.correct_pos_cnt} correct positions & {round_.incorrect_pos_cnt} incorrect positions.')

    @staticmethod
    def display_game_result() -> None:
        print(f'{game.result_dict}')


class Color:
    def __init__(self, letter: str, image: str):
        self.letter = letter
        self.image = image

    def __repr__(self):
      return f'Color Object: {self.letter}'


class ColorBank:
    all_color_letters = ['r', 'y', 'g', 'c', 'b', 'p']
    def __init__(self):
        self.color_objects = []
      
    @property
    def color_letter_list(self):
        return [c.letter for c in self.color_objects]

    def add_color(self, color_obj: Color):
      self.color_objects.append(color_obj)
      
    def remove_color(self, idx: int):
      self.color_objects.pop(idx)
      
    def get_color_from_letter(self, letter: str) -> Color:
        return [c for c in self.color_objects if letter == c.letter][0]


# should there be a parent Game class that creates the shell for all games?
# email, app_name, start, end, ?maybe outcome?
class Game:
    def __init__(self):
      self.user_email = ''
      self.app_name = 'mastermind'
      self.start_time = ''  # datetime.utcnow()
      self.end_time = ''
      self.color_set_cnt = 0  # color_set_cnt
      self.answer_len = 0  # answer_len
      self.generated_answer = ColorBank()
      self.max_guess_cnt = 0  # max_guess_cnt
      self.guess_cnt = 0
      self.round_list = []
      self.outcome = ''
      self.phase = 'new_game'  # if guessing, "play" button should be disabled

    def generate_answer(self):
      for i in range(self.answer_len):
        c = random.choice(available_color_bank.color_objects)
        self.generated_answer.add_color(c)

    def append_round(self, round_obj: dict):
      self.round_list.append(round_obj)

    def increment_guess_cnt(self):
        self.guess_cnt += 1

    def evaluate_end_game(self, correct_pos_cnt):
      if correct_pos_cnt == self.answer_len:
        self.update_outcome('win')
      elif self.guess_cnt >= self.max_guess_cnt:
        self.update_outcome('loss')

    def update_outcome(self, outcome: str):
      self.outcome = outcome
      self.phase = 'game_over'
      anvil.server.call('write_game_data', self.result_dict)

    @property
    def result_dict(self):
        return {'email': self.user_email, 'app': self.app_name,
                'start_time': self.start_time, 'end_time': datetime.utcnow(),
                'color_set_cnt': self.color_set_cnt, 'answer': self.generated_answer.color_letter_list, 'answer_len': self.answer_len,
                'max_guess_cnt': self.max_guess_cnt, 'actual_guess_cnt': self.guess_cnt,
                'outcome': self.outcome}


class Round:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
      
    def __init__(self):
        self.guess_number = game.guess_cnt + 1
        self.guess = guess.color_objects
        self.correct_pos_cnt = 0
        self.incorrect_pos_cnt = 0

    def compare_answer_and_guess(self) -> None:
      game.increment_guess_cnt()
      total_correct_cnt = 0
      guess_letters = guess.color_letter_list.copy()
      answer_letters = game.generated_answer.color_letter_list.copy()
      print(answer_letters, guess_letters)
      for l in guess_letters:
          if l in answer_letters:
              answer_letters.remove(l)
              total_correct_cnt += 1
      for i in range(game.answer_len):
          if guess.color_letter_list[i] == game.generated_answer.color_letter_list[i]:
              self.correct_pos_cnt += 1
      self.incorrect_pos_cnt = total_correct_cnt - self.correct_pos_cnt
      game.append_round({'guess_number': self.guess_number, 'guess': self.guess.copy(),
                         'correct_pos_cnt': self.correct_pos_cnt, 'incorrect_pos_cnt': self.incorrect_pos_cnt})

    def end_round(self) -> None:
      guess.color_objects.clear()
      game.evaluate_end_game(self.correct_pos_cnt)
      

def create_new_game(email, color_set_cnt, answer_len, max_guess_cnt):
  game.__init__()
  available_color_bank.color_objects = [Color(c, f'_/theme/mastermind/mm_{c}.png') for idx, c in enumerate(ColorBank.all_color_letters) if idx + 1 <= color_set_cnt]
  # game = Game(email=email, max_guess_cnt=max_guess_cnt, color_set_cnt=color_set_cnt, answer_len=answer_len)
  game.user_email = email
  game.start_time = datetime.utcnow()
  game.color_set_cnt, game.answer_len, game.max_guess_cnt = color_set_cnt, answer_len, max_guess_cnt
  game.generate_answer()
  game.phase = 'guessing'
  

def create_new_round():
  round_.__init__()

# i want to create a game instance only when a new game is created, but i can't figure out how to create it on demand (outside of a function)
# to create 'game' in the global scope, my workaround is to create a shell of a game instance and then actually populate it upon call
game = Game()
available_color_bank = ColorBank()
guess = ColorBank()
round_ = Round.__new__(Round)

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

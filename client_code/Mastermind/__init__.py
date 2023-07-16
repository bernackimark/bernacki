from ._anvil_designer import MastermindTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from . import mastermind_module as m
from .. import utils_for_anvil as util
import anvil.image

class Mastermind(MastermindTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    user = anvil.users.get_user()
    self.email = user['email'] if user else 'bernackimark@gmail.com'
    # print(f'The email is: {email}')
    
    self.prompt_1_lbl.text = m.UI.prompt_datatype_answers[0]['prompt']
    self.prompt_2_lbl.text = m.UI.prompt_datatype_answers[1]['prompt']
    self.prompt_3_lbl.text = m.UI.prompt_datatype_answers[2]['prompt']
    self.prompt_1_dd.items = util.convert_list_of_ints_to_tuples_for_dd(m.UI.prompt_datatype_answers[0]['answers'])
    self.prompt_2_dd.items = util.convert_list_of_ints_to_tuples_for_dd(m.UI.prompt_datatype_answers[1]['answers'])
    self.prompt_3_dd.items = util.convert_list_of_ints_to_tuples_for_dd(m.UI.prompt_datatype_answers[2]['answers'])
    self.prompt_1_dd.selected_value, self.prompt_2_dd.selected_value, self.prompt_3_dd.selected_value = 6, 4, 10
    self.rt_instructions.content = m.UI.instructions_text
  
  def new_game_btn_click(self, **event_args):
    m.create_new_game(self.email, self.prompt_1_dd.selected_value, self.prompt_2_dd.selected_value, self.prompt_3_dd.selected_value)
    self.display_available_colors()
    self.card_new_game.visible = self.card_play_again.visible = False
    self.card_round_number.visible = self.card_available_colors.visible = self.card_your_guess.visible = self.card_guess_log.visible = True
    self.display_game_status()
    self.display_guess_log()

  def display_available_colors(self):
    self.available_colors_gp.clear()
    for idx, c in enumerate(m.available_color_bank.color_objects):
      image = Image(source=c.image, height=50, display_mode='shrink_to_fit')
      # using a grid panel because i couldn't get the images to appear on a flow panel.  not sure why.
      link = Link()
      link.tag.letter = c.letter
      link.add_event_handler('click', self.add_color_to_guess)
      link.add_component(image)
      self.available_colors_gp.add_component(link, row='A', col_xs=idx*2, width_xs=2)
      # can i easily make an Image have an on_click event?  or do i need to use a different component?

  def add_color_to_guess(self, **event_args):
    if len(m.guess.color_objects) >= m.game.answer_len:
      alert('Your guess is currently full.  To remove a color, click on it in your guess list.')
      return
    color_obj = m.available_color_bank.get_color_from_letter(event_args['sender'].tag.letter)
    m.guess.add_color(color_obj)
    self.display_guess()

  def remove_color_from_guess(self, **event_args):
    m.guess.remove_color(event_args['sender'].tag.idx)
    self.display_guess()

  def display_guess(self):
    self.guess_gp.clear()

    for idx, c in enumerate(m.guess.color_objects):
      image = Image(source=c.image, height=50, display_mode='shrink_to_fit')
      # using a grid panel because i couldn't get the images to appear on a flow panel.  not sure why.
      link = Link()
      link.tag.letter, link.tag.idx = c.letter, idx
      link.add_event_handler('click', self.remove_color_from_guess)
      link.add_component(image)
      self.guess_gp.add_component(link, row='A', col_xs=idx*2, width_xs=2)    
    self.submit_guess_btn.enabled = (len(m.guess.color_objects) == m.game.answer_len)
    self.btn_clear_guess.enabled = (len(m.guess.color_objects) > 0)

  def submit_guess_btn_click(self, **event_args):
    m.create_new_round()
    m.round_.compare_answer_and_guess()
    self.display_guess_log()
    m.round_.end_round()
    self.display_guess()
    self.display_game_status()

  def btn_clear_guess_click(self, **event_args):
    m.guess.remove_all()
    self.display_guess()
  
  def display_guess_log(self):          
    self.rp_guess_log.items = sorted(m.game.round_list, key=lambda x: x['guess_number'], reverse=True)

  def display_game_status(self):
    self.gp_winning_combo.clear()
    if m.game.phase == 'guessing':
      self.lbl_game_status.text = f'Round {m.game.guess_cnt + 1} of {m.game.max_guess_cnt}'
      return
    if m.game.phase == 'game_over':
      self.card_available_colors.visible = self.card_your_guess.visible = False
      if m.game.outcome == 'win':
        self.lbl_game_status.text = f'Congrats!  You won on Guess #{m.game.guess_cnt}.'
      elif m.game.outcome == 'loss':
        for idx, c in enumerate(m.game.generated_answer.color_objects):
          image = Image(source=c.image, height=50, display_mode='shrink_to_fit')
          # using a grid panel because i couldn't get the images to appear on a flow panel.  not sure why.
          link = Link()
          link.add_component(image)
          self.gp_winning_combo.add_component(link, row='A', col_xs=idx*2, width_xs=2)
        self.lbl_game_status.text = f'Bummer.  You have run out of guesses.  The correct answer was:'
        self.gp_winning_combo.visible = True
      self.card_play_again.visible = True

  def btn_play_again_click(self, **event_args):
    self.card_new_game.visible = True
    self.card_play_again.visible = False

  def btn_close_instructions_click(self, **event_args):
    self.card_instructions.visible = False


    
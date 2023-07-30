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
from ... import utils_for_anvil as util
# import anvil.image

class Mastermind(MastermindTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    user = anvil.users.get_user()
    self.email = user['email'] if user else None
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
    m.mastermind = m.Mastermind(self.email, self.prompt_1_dd.selected_value, self.prompt_2_dd.selected_value, self.prompt_3_dd.selected_value)
    self.display_available_colors()
    self.card_new_game.visible = self.card_play_again.visible = False
    self.card_round_number.visible = self.card_available_colors.visible = self.card_your_guess.visible = self.card_guess_log.visible = True
    self.display_game_status()
    self.display_guess_log()

  def display_available_colors(self):
    self.available_colors_gp.clear()
    for idx, c in enumerate(m.mastermind.color_bank.game_color_objects):
      image = Image(source=c.image, height=50, display_mode='shrink_to_fit')
      # using a grid panel because i couldn't get the images to appear on a flow panel.  not sure why.
      link = Link()
      link.tag.color = c.color
      link.add_event_handler('click', self.add_color_to_guess)
      link.add_component(image)
      self.available_colors_gp.add_component(link, row='A', col_xs=idx*2, width_xs=2)
      # can i easily make an Image have an on_click event?  or do i need to use a different component?

  def add_color_to_guess(self, **event_args):
    color_str = event_args['sender'].tag.color
    if not m.guess.add_guess_str(color_str):
      alert('Your guess is currently full.  To remove a color, click on it in your guess list.')
      return
    self.display_guess()

  def remove_color_from_guess(self, **event_args):
    m.guess.remove_guess_object(event_args['sender'].tag.idx)
    self.display_guess()

  def display_guess(self):
    self.guess_gp.clear()

    for idx, c in enumerate(m.guess.color_objects):
      image = Image(source=c.image, height=50, display_mode='shrink_to_fit')
      # using a grid panel because i couldn't get the images to appear on a flow panel.  not sure why.
      link = Link()
      link.tag.color, link.tag.idx = c.color, idx
      link.add_event_handler('click', self.remove_color_from_guess)
      link.add_component(image)
      self.guess_gp.add_component(link, row='A', col_xs=idx*2, width_xs=2)    
    self.submit_guess_btn.enabled = (len(m.guess.color_objects) == m.mastermind.answer_len)
    self.btn_clear_guess.enabled = (len(m.guess.color_objects) > 0)

  def submit_guess_btn_click(self, **event_args):
    m.mastermind.evaluate_answer_log_result()
    self.display_guess_log()
    m.guess.clear_my_guess()
    m.mastermind.check_for_end_game()
    self.display_guess()
    self.display_game_status()

  def btn_clear_guess_click(self, **event_args):
    m.guess.clear_my_guess()
    self.display_guess()
  
  def display_guess_log(self):          
    self.rp_guess_log.items = sorted(m.mastermind.round_list, key=lambda x: x['guess_number'], reverse=True)

  def display_game_status(self):
    self.gp_winning_combo.clear()
    if m.mastermind.state == 'guessing':
      self.lbl_game_status.text = f'Round {m.mastermind.guess_number + 1} of {m.mastermind.max_guess_cnt}'
      return
    if m.mastermind.state == 'game_over':
      self.card_available_colors.visible = self.card_your_guess.visible = False
      if m.mastermind.outcome == 'win':
        self.lbl_game_status.text = f'Congrats!  You won on Guess #{m.mastermind.guess_number}.'
      elif m.mastermind.outcome == 'loss':
        for idx, c in enumerate(m.mastermind.generated_answer):
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

from ._anvil_designer import MastermindTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import mastermind_module as m
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

    self.colors_in_guess = 0
  
  def new_game_btn_click(self, **event_args):
    m.create_new_game('', self.prompt_1_dd.selected_value, self.prompt_2_dd.selected_value, self.prompt_3_dd.selected_value)
    # m.create_new_game(self.email, self.prompt_1_dd.selected_value, self.prompt_2_dd.selected_value, self.prompt_3_dd.selected_value)
    self.display_available_colors()
    self.new_game_btn.enabled = False

  def display_available_colors(self):
    for idx, c in enumerate(m.color_bank.game_color_objects):
      image = Image(source=c.image, height=50, display_mode='shrink_to_fit')
      # using a grid panel because i couldn't get the images to appear on a flow panel.  not sure why.
      link = Link()
      link.tag.color = c.color
      link.add_event_handler('click', self.add_color_to_guess)
      link.add_component(image)
      self.available_colors_gp.add_component(link, row='A', col_xs=idx*2, width_xs=2)
      # can i easily make an Image have an on_click event?  or do i need to use a different component?

  def add_color_to_guess(self, **event_args):
    if self.colors_in_guess > m.game.answer_len:
      return
    color = event_args['sender'].tag.color
    m.guess.add_guess_object(color)
    print(m.guess.color_objects)
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
      link.tag.color = c.color
      link.tag.idx = idx
      link.add_event_handler('click', self.remove_color_from_guess)
      link.add_component(image)
      self.guess_gp.add_component(link, row='A', col_xs=idx*2, width_xs=2)    




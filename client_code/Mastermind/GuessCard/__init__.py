from ._anvil_designer import GuessCardTemplate
from anvil import *
import anvil.server

class GuessCard(GuessCardTemplate, guess_num, correct_pos_cnt, incorrect_pos_cnt, colors=None):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.guess_num_lbl.text = guess_num
    # self.colors_cp.add_component(Image())
    self.correct_pos_lbl.text = correct_pos_cnt
    self.incorrect_pos_lbl.text = incorrect_pos_cnt
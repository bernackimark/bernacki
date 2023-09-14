from ._anvil_designer import SetbackBotChallengeCardTemplate
from anvil import *
from .. import Setback
from ..SetbackBotChallenge import SetbackBotChallenge
from anvil.tables import app_tables

class SetbackBotChallengeCard(SetbackBotChallengeCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    self.role = 'card'
    self.button_column_spacer.width = 50
    self.name_levels_container.col_widths = 125

    # Any code you write here will run when the form opens.
    if self.play_button.enabled == False:
      self.play_button.tooltip = 'To unlock this opponent, defeat the prior ten times'
    
  def play_button_click(self, **event_args):
    self.parent.visible = False
    get_open_form().add_component(Setback())
    


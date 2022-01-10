from ._anvil_designer import SetbackBotChallengeCardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SetbackBotChallengeCard(SetbackBotChallengeCardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.role = 'card'
    self.button_column_spacer.width = 50
    self.name_levels_container.col_widths = 125

    # Any code you write here will run when the form opens.
    if self.play_button.enabled == False:
      self.play_button.tooltip = 'To unlock this opponent, defeat the prior ten times'

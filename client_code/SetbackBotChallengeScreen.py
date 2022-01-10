from ._anvil_designer import SetbackBotChallengeScreenTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SetbackBotChallengeScreen(SetbackBotChallengeScreenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.repeating_panel.items = app_tables.bots.search()
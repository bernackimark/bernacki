from ._anvil_designer import SetbackBotChallengeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SetbackBotChallenge(SetbackBotChallengeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.bot_challenge_panel.items = app_tables.bots.search()

    # Any code you write here will run when the form opens.
    
  def show_setback(self):
    self.content_panel.add_component(Setback())
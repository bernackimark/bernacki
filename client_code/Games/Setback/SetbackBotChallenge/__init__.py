from ._anvil_designer import SetbackBotChallengeTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
from anvil.tables import app_tables

class SetbackBotChallenge(SetbackBotChallengeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.bot_challenge_panel.items = app_tables.bots.search()
    
  def show_setback(self):
    self.content_panel.add_component(Setback())
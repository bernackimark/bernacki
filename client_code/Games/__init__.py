from ._anvil_designer import GamesTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
from .Cribbage import Cribbage
from .Mastermind import Mastermind
from .Setback import Setback
from .Setback.SetbackBotChallenge import SetbackBotChallenge


class Games(GamesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # not using the stuff repeating panel right now.  i can't get the image to show !!
    # self.stuff_repeating_panel.items = anvil.server.call('get_stuff_details').search()
    # stuff_info = anvil.server.call('get_stuff_details').search()
    
    self.setback_lmt_label.text = "last modified: " + str(anvil.server.call('get_stuff_lmt', 'setback'))
    self.cribbage_lmt_label.text = "last modified " + str(anvil.server.call('get_stuff_lmt', 'cribbage'))

  def launch_cribbage_click(self, **event_args):
    pass
    # self.content_panel.clear()
    # self.content_panel.add_component(Cribbage())

  def launch_setback_click(self, **event_args):
    self.content_panel.clear()
    self.stuff_repeating_panel.visible = False
    self.content_panel.add_component(SetbackBotChallenge())

  def launch_mastermind_click(self, **event_args):
    self.content_panel.clear()
    self.stuff_repeating_panel.visible = False
    self.content_panel.add_component(Mastermind())


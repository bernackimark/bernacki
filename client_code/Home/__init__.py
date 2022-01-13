from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Setback import Setback
from ..Setback.SetbackBotChallenge import SetbackBotChallenge
from ..Cribbage import Cribbage

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # not using the stuff repeating panel right now.  i can't get the image to show !!
    # self.stuff_repeating_panel.items = anvil.server.call('get_stuff_details').search()
    # stuff_info = anvil.server.call('get_stuff_details').search()
    
    self.questions_lmt_label.text = "last modified: " + str(anvil.server.call('get_stuff_lmt', 'questions'))
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

  def launch_questions_click(self, **event_args):
    pass


  





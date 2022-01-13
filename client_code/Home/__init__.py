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
from ..Cribbage import Cribbage

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.stuff_repeating_panel.items = app_tables.stuff.search()

    self.stuff_repeating_panel.items = anvil.server.call('get_stuff_details').search()
      
    
  def launch_cribbage_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Cribbage())

  def launch_setback_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Setback())

  def launch_questions_click(self, **event_args):
    pass


  





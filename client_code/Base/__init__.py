from ._anvil_designer import BaseTemplate
from anvil import *
from ..Home import Home

class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.content_panel.add_component(Home())
    #self.form_show() # this shouldn't be needed, but Help Forum suggests it
    
    # Any code you write here will run when the form opens.

  def title_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Home())

  def my_games_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Home())
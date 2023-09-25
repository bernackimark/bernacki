from ._anvil_designer import CribbageTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server

class Cribbage(CribbageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
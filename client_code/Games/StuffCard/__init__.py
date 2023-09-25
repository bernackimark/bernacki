from ._anvil_designer import StuffCardTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server

class StuffCard(StuffCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

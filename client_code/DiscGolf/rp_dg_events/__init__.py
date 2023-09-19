from ._anvil_designer import rp_dg_eventsTemplate
from anvil import *

class rp_dg_events(rp_dg_eventsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

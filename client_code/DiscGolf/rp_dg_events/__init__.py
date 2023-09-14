from ._anvil_designer import rp_dg_eventsTemplate
from anvil import *

class rp_dg_events(rp_dg_eventsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

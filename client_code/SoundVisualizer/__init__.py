from ._anvil_designer import SoundVisualizerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SoundVisualizer(SoundVisualizerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    shapes = ['rect', 'circle']
    schemes = ['maroon', 'gold']
    scales = ['major', 'minor']
    [self.fp_shape.add_component(Button(text=s)) for s in shapes]
    [self.fp_scheme.add_component(Button(text=s)) for s in schemes]
    self.dd_scale.items = [(str(s.title), s) for s in scales]

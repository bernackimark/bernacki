from ._anvil_designer import build_a_trip_row_templateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import random
from itertools import cycle

POINT_NAME_PLACEHOLDERS = ['123 Main St, Anywhere, ST, USA', 'New Britain Museum of American Art', 'Charleston, SC',
                           'The Waldorf Astoria in New York City', '1600 Pennsylvania Avenue, Washington, DC, 37188', 'Dodger Stadium Los Angeles']
next_placeholder = cycle(POINT_NAME_PLACEHOLDERS)

class build_a_trip_row_template(build_a_trip_row_templateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.tb_point_name.placeholder = next(next_placeholder)

  def btn_delete_point_click(self, **event_args):
    
    self.parent.raise_event('x-refresh-trip-builder')

    
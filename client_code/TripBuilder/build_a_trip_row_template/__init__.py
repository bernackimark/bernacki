from ._anvil_designer import build_a_trip_row_templateTemplate
from anvil import *
import anvil.server

from ... import trip_builder_module as m

import random
from itertools import cycle

POINT_NAME_PLACEHOLDERS = ['123 Main St, Anywhere, ST, USA', 'New Britain Museum of American Art', 'Charleston, SC',
                           'The Waldorf Astoria in New York City', '1600 Pennsylvania Avenue, Washington, DC, 37188', 'Dodger Stadium Los Angeles']
next_placeholder = cycle(POINT_NAME_PLACEHOLDERS)

class build_a_trip_row_template(build_a_trip_row_templateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.tb_point_name.placeholder = next(next_placeholder)
    if self.lbl_lat_long.text in [(), None]:
      self.lbl_lat_long.visible = False
    else:
      self.lbl_lat_long.visible = True

  def btn_delete_point_click(self, **event_args):
    m.delete_item(self.item)
    self.parent.raise_event('x-refresh-trip-builder')

    
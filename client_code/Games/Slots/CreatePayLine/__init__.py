from ._anvil_designer import CreatePayLineTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..slots import create_pay_line as m

class CreatePayLine(CreatePayLineTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # why does this fail with the error "'function' object has no attribute"?!?!?!
    self.matrix = m.TileMatrix(3, 5)

    
    for r_idx, row in enumerate(self.matrix):
      for c_idx, tile in enumerate(row):
        link = Link()
        link.add_component(Image(source=tile.img))
        link.add_event_handler('click', tile.click_tile())
        link.tag = (r_idx, c_idx)
        self.gp_create_shape.add_component(link,
                                           row=self.matrix.rows[r_idx],
                                           col_xs=self.matrix.cols[c_idx],
                                           width_xs=1)


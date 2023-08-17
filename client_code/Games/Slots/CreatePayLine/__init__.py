from ._anvil_designer import CreatePayLineTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..slots import user_pay_line as m


class CreatePayLine(CreatePayLineTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.matrix = m.TileMatrix(3, 5)
    self.display_matrix()
    

  def display_matrix(self):
    self.gp_create_shape.clear()
    for r_idx, row in enumerate(self.matrix):
      for c_idx, tile in enumerate(row):
        link = Link()
        link.tag.row, link.tag.col = r_idx, c_idx
        link.add_component(Image(source=tile.img))
        link.add_event_handler('click', self.tile_click)
        self.gp_create_shape.add_component(link,
                                           row=self.matrix.rows[r_idx],
                                           col_xs=self.matrix.cols[c_idx]*2,
                                           width_xs=2)    

  def tile_click(self, **e):
    print('ABC')
    link_object = e['sender']
    row, col = link_object.tag.row, link_object.tag.col
    self.matrix.tiles[row][col].click_tile()
    self.display_matrix()
from ._anvil_designer import CreatePayLineTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server

from ..slots import user_pay_line as m


class CreatePayLine(CreatePayLineTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    m.tile_matrix = m.TileMatrix(3, 5)
    # self.matrix = m.TileMatrix(3, 5)
    self.display_matrix()
    
  def display_matrix(self):
    self.gp_create_shape.clear()
    # for r_idx, row in enumerate(self.matrix):
    for r_idx, row in enumerate(m.tile_matrix):
      for c_idx, tile in enumerate(row):
        link = Link()
        link.tag.row, link.tag.col = r_idx, c_idx
        link.add_component(Image(source=tile.img))
        link.add_event_handler('click', self.tile_click)
        self.gp_create_shape.add_component(link,
                                           # row=self.matrix.rows[r_idx],
                                           row=m.tile_matrix.rows[r_idx],
                                           # col_xs=self.matrix.cols[c_idx]*2-2,
                                           col_xs=m.tile_matrix.cols[c_idx]*2-2,
                                           width_xs=2)    

  def tile_click(self, **e):
    link_object = e['sender']
    row, col = link_object.tag.row, link_object.tag.col
    # self.matrix.click_tile(row, col)
    m.tile_matrix.click_tile(row, col)
    self.display_matrix()
    m.tile_matrix.status = ''

  def tb_pay_line_name_lost_focus(self, **event_args):
    m.tile_matrix.name = self.tb_pay_line_name.text
    m.tile_matrix.status = ''
  
  def dd_winning_multiplier_change(self, **event_args):
    m.tile_matrix.multiplier = self.dd_winning_multiplier.selected_value
  
  def btn_create_pay_line_click(self, **event_args):
    if not m.tile_matrix.is_valid:
      alert(m.tile_matrix.status)
      return
    m.tile_matrix.status = 'submitted'
    self.visible = False



    


from ._anvil_designer import CreatePieceTemplate
from anvil import *
import anvil.server

from .. import slots as m

class CreatePiece(CreatePieceTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def btn_create_pay_line_click(self, **event_args):
    if not self.tb_piece_name.text:
      alert('Please name your piece')
      return
    if not self.fl_piece.file:
      alert('Please upload an image')
      return

    '''FileLoader.file is a media object.
    anvil.image.generate_thumbnail generates an unusably poor pixelated image.'''      
    media_obj = anvil.server.call('resize_media_obj_image', self.fl_piece.file, m.PIECE_HEIGHT, m.PIECE_WIDTH)

    m.create_piece(self.tb_piece_name.text, self.dd_piece_multiplier.selected_value, self.cb_wild.checked, media_obj)
    self.raise_event("x-close-alert")
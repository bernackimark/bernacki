from ._anvil_designer import CreatePieceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import slots as m

class CreatePiece(CreatePieceTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def fl_piece_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass

  def btn_create_pay_line_click(self, **event_args):
    if not self.tb_piece_name.text:
      alert('Please name your piece')
    if not self.fl_piece.file:
      alert('Please upload an image')

    # do i need to scale down the image, etc?
    
    m.create_piece(self.tb_piece_name.text, self.dd_piece_multiplier.selected_value, self.cb_wild.checked, self.fl_piece.file)
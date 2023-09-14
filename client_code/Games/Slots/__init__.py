from ._anvil_designer import SlotsTemplate
from anvil import *

from .CreatePayLine import CreatePayLine
from .CreatePiece import CreatePiece

from .slots import user_pay_line as upl
from . import slots as m
from ...user import user
import random
from itertools import cycle

class Slots(SlotsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    self.initial_setup()
    self.tb_bet_amt.text = 1
    self.lbl_balance.text = m.slots.slots_balance


  def initial_setup(self) -> None:
    m.slots = m.Slots(self.user['email'], self.user['info'].get('slots_balance'))

  def tb_bet_amt_change(self, **event_args):
    if self.tb_bet_amt.text in [None, '', ' ', 0]:
      self.bet_error('Please make a valid bet')
      return

    if not int(self.tb_bet_amt.text) == self.tb_bet_amt.text:
      self.bet_error('Your bet must bet a whole number')
      return
    
    if not 1 <= self.tb_bet_amt.text <= float(self.lbl_balance.text):
      self.bet_error('Please bet between 1 and your current balance.')
      return

    self.lbl_balance.text = m.slots.slots_balance - self.tb_bet_amt.text

  def bet_error(self, msg) -> None:
    alert(msg)
    self.tb_bet_amt.text = 0
    self.lbl_balance.text = m.slots.slots_balance - self.tb_bet_amt.text
    
  def btn_spin_click(self, **event_args):
      # self.reel_snapshot_idx = 0  # this was in the tkinter version, might need this
      m.slots.spin(self.tb_bet_amt)
      # self.display_reels()  # needs to be defined
      m.slots.check_for_winners()
      # self.display_payout()  # needs to be defined
      print('I am trying to end the round')
      m.slots.end_round()

  # SPINNING IS THE NEXT PLACE TO ADDRESS !!!

  def btn_create_pay_line_click(self, **event_args):
    c = alert(content=CreatePayLine(), large=True, buttons=[('Close', 'Close')])
    if upl.tile_matrix.status == 'submitted':
      shape = m.create_game_shape(upl.tile_matrix.name, upl.tile_matrix.y_offsets, upl.tile_matrix.multiplier)
      pay_lines = m.create_pay_line(shape, m.REEL_WINDOW_HEIGHT)
      print(pay_lines)

  def btn_create_piece_click(self, **event_args):
    c = alert(content=CreatePiece(), large=True, buttons=[('Close', 'Close')])


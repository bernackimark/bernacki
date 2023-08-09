from ._anvil_designer import SlotsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .CreatePayLine import CreatePayLine

from . import slots as m
import random
from itertools import cycle

class Slots(SlotsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    self.initial_setup()
    self.tb_bet_amt.text = 0
    self.lbl_balance.text = m.slots.slots_balance


  def initial_setup(self) -> None:
    [m.pieces.append(p) for p in m.default_pieces]
    [m.spin_shapes.append(s) for s in m.default_shapes]
    [m.create_pay_line(s, m.REEL_WINDOW_HEIGHT) for s in m.spin_shapes]
    piece_in_cycle = cycle(m.pieces)
    [m.reels.append(m.Reel(r, [next(piece_in_cycle) for _ in range(m.REEL_LENGTH + 1)], random.randint(5, 50))) for r in range(m.REEL_CNT)]
    m.slots.player_emails.append(self.user['email'])
    m.slots.slots_balance = self.user['info'].get('slots_balance')

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
    m.spin_reels(self.tb_bet_amt.text)

  def btn_create_pay_line_click(self, **event_args):
    alert(content=CreatePayLine(), title='Create My Own Payline', large=True)



from ._anvil_designer import SlotsTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server

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
        self.user = user.user
        self.initial_setup()
        self.tb_bet_amt.text = 1
        self.lbl_balance.text = m.slots.slots_balance
        self.reels = [[None for piece in row] for row in m.slots.reels.transposed_visible_reels]
        self.populate_gp_reels()
        self.display_reels(m.slots.reels.transposed_visible_reels)
    
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
        m.slots.spin(self.tb_bet_amt.text)
        for snapshot in m.slots.reels.snapshots:
            transposed_snapshot = m.slots.reels.transposed_visible_snapshot(snapshot)
            self.display_reels(transposed_snapshot)
        # self.display_reels()  # needs to be defined
        m.slots.check_for_winners()
        # self.display_payout()  # needs to be defined
        print('I am trying to end the round')
        m.slots.end_round()

    def populate_gp_reels(self):
        for r_idx, row in enumerate(self.reels):
            for c_idx, piece in enumerate(row):
                lbl = Label(align='center', font_size=36, background='red')
                self.reels[r_idx][c_idx] = lbl
                self.gp_reels.add_component(lbl, row=r_idx, col_xs=c_idx, width_xs=2)        

    def display_reels(self, reels: list[list[m.Piece]]):
        for r_idx, reel in enumerate(reels):
            for c_idx, piece in enumerate(reel):
                self.reels[r_idx][c_idx].text = piece.text
                
                
                
                
    
    def btn_create_pay_line_click(self, **event_args):
        c = alert(content=CreatePayLine(), large=True, buttons=[('Close', 'Close')])
        if upl.tile_matrix.status == 'submitted':
            shape = m.create_game_shape(upl.tile_matrix.name, upl.tile_matrix.y_offsets, upl.tile_matrix.multiplier)
            pay_lines = m.create_pay_line(shape, m.REEL_WINDOW_HEIGHT)
            print(pay_lines)
    
    def btn_create_piece_click(self, **event_args):
        c = alert(content=CreatePiece(), large=True, buttons=[('Close', 'Close')])


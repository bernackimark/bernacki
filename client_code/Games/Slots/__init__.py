from ._anvil_designer import SlotsTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server

from .CreatePayLine import CreatePayLine
from .CreatePiece import CreatePiece

from .slots import user_pay_line as upl
from . import slots as m
import random
from itertools import cycle
import time

class Slots(SlotsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.initial_setup()
        self.lbl_bet_amt.text = 1
        self.lbl_balance.text = m.slots.slots_balance
        self.reels = [[None for piece in row] for row in m.slots.reels.transposed_visible_reels]
        self.populate_gp_reels()
        self.display_reels(m.slots.reels.transposed_visible_reels)
    
    def initial_setup(self) -> None:
        m.slots = m.Slots()

    def btn_increase_bet_click(self, **event_args):
        if self.lbl_bet_amt.text > float(self.lbl_balance.text):
            return
        if self.lbl_bet_amt.text >= m.slots.max_bet:
            self.lbl_bet_amt.text = m.slots.min_bet
            return
        self.lbl_bet_amt.text += 1
    
    def btn_spin_click(self, **event_args):
        print(m.slots.slots_balance)
        
        m.slots.spin(self.lbl_bet_amt.text)
        for snapshot in m.slots.reels.snapshots:
            transposed_snapshot = m.slots.reels.transposed_visible_snapshot(snapshot)
            self.display_reels(transposed_snapshot)
            time.sleep(.03)
            '''Sleep is required else the browser won't show any changes'''

        m.slots.check_for_winners()

        print(m.slots.slots_balance)
        # self.display_payout()  # needs to be defined
        m.slots.end_round()

    def populate_gp_reels(self):
        for r_idx, row in enumerate(self.reels):
            for c_idx, piece in enumerate(row):
                img = Image(align='center', height=m.PIECE_HEIGHT, width=m.PIECE_WIDTH)
                self.reels[r_idx][c_idx] = img
                self.gp_reels.add_component(img, row=r_idx, col_xs=c_idx+3, width_xs=1)   
                # self.xyp_reels.add_component(img, x=c_idx * 10 + 20, y=r_idx * 10 + 5)

    def display_reels(self, reels: list[list[m.Piece]]):
        for r_idx, reel in enumerate(reels):
            for c_idx, piece in enumerate(reel):
                self.reels[r_idx][c_idx].source = piece.img
 
                
                
    
    def btn_create_pay_line_click(self, **event_args):
        c = alert(content=CreatePayLine(), large=True, buttons=[('Close', 'Close')])
        if upl.tile_matrix.status == 'submitted':
            shape = m.create_game_shape(upl.tile_matrix.name, upl.tile_matrix.y_offsets, upl.tile_matrix.multiplier)
            pay_lines = m.create_pay_line(shape, m.REEL_WINDOW_HEIGHT)
            print(pay_lines)
    
    def btn_create_piece_click(self, **event_args):
        c = alert(content=CreatePiece(), large=True, buttons=[('Close', 'Close')])


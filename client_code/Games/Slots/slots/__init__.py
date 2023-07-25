import anvil.server
import anvil.users

import random
from datetime import datetime

from .slots_ui import UI
from .slots_classes import PayLine, Piece, Reel, Shape, Slots, Spin
from .slots_default_items import default_pieces, default_shapes


REEL_CNT = 5
REEL_LENGTH = 100
REEL_WINDOW_HEIGHT = 5
ROTATIONS: list[tuple] = [(i*100+1, i*100+100) for i in range(1, REEL_CNT + 1)]
MIN_SAME_LINE_MATCH = 3


def create_piece(id: int, img: str, mult: int = 1, wild: bool = False) -> Piece:
    return Piece(id, img, mult, wild)


def create_game_shape(name: str, y_offsets: list[int], multiplier: int = 3):
    if len(y_offsets) < MIN_SAME_LINE_MATCH:
        UI.display(f'Your shape must be at least {MIN_SAME_LINE_MATCH} reels wide.')
        return
    spin_shapes.append(Shape(name, y_offsets, multiplier))


def create_pay_line(s: Shape, reel_window_height: int):
    pay_line_id = 1 if len(pay_lines) == 0 else max([pl.line_number for pl in pay_lines]) + 1
    starting_y = 0
    while starting_y + max(s.y_offsets) <= reel_window_height - 1:
        pay_lines.append(
            PayLine(pay_line_id, s, [(idx, starting_y + y_offset) for idx, y_offset in enumerate(s.y_offsets)]))
        pay_line_id += 1
        starting_y += 1


slots = Slots()
slots.state = 'betting'
slots.slots_balance: float = 0  # nightly job that adds more coins to low balances?
pieces: list[Piece] = []  # [_ for _ in default_pieces]
spin_shapes: list[Shape] = []  # [_ for _ in default_shapes]
pay_lines: list[PayLine] = []
reels: list[Reel] = []

# ^^^ setup
# vvv user clicks Spin

# the rest of this needs to be handled in a single function
def spin_reels(bet_amt: int) -> None:
    slots.slots_balance -= bet_amt
    # spin the reels
    slots.state = 'spinning'
    spin = Spin(slots.player_emails[0], slots.slots_balance, bet_amt, pay_lines.copy())
    rotation_counts = [random.randint(ROTATIONS[i][0], ROTATIONS[i][1]) for i in range(REEL_CNT)]
    [r.rotate() for i in range(max(rotation_counts)) for r in reels if i <= rotation_counts[r.pos]]

    # capture the resting reels
    slots.state = 'paying'
    spin.update_matrix(reels, REEL_CNT, REEL_WINDOW_HEIGHT)
    UI.display_spun_matrix(spin.spun_matrix)

    # check for winners
    for pl in pay_lines:
        pl.update_pieces([spin.spun_matrix[coord[1]][coord[0]] for coord in pl.coordinates])
    winning_pay_lines: list[PayLine] = [pl for pl in pay_lines if pl.is_winner]

    # payout
    spin_payout = 0
    for wpl in winning_pay_lines:
        line_payout: int = spin.bet_amt * wpl.winning_multiplier
        msg: str = f'Line {wpl.line_number} pays out {line_payout}'
        UI.display(msg)
        spin_payout += line_payout
        # cycle through those messages on the screen?

    UI.display(f'Your total win is {spin_payout}')
    bal_before_payout = slots.slots_balance
    slots.slots_balance = slots.slots_balance + spin_payout
    UI.display(f'Your new balance is {slots.slots_balance}')

    slots.game_end_ts = datetime.utcnow()
    slots.game_data = {'starting_bal': bal_before_payout,
                      'spin_bet': spin.bet_amt,
                      'spin_matrix': spin.spun_matrix_ids,
                      'payout': spin_payout,
                      'ending_bal': slots.slots_balance}
    updated_player_data = {'slots_balance': slots.slots_balance}
    
    anvil.server.call('write_game_data', slots.as_dictionary, updated_player_data)

    slots.state = 'betting'

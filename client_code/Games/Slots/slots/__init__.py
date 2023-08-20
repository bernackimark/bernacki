import anvil.server

import random
from datetime import datetime
import time
from itertools import cycle
from copy import deepcopy

# from ... import game_super_class as gsc
from ... game_super_class import Game

REEL_CNT = 5
REEL_LENGTH = 100
REEL_WINDOW_HEIGHT = 5
ROTATIONS: list[tuple] = [(i * 100 + 1, i * 100 + 100) for i in range(1, REEL_CNT + 1)]
MIN_SAME_LINE_MATCH = 3
MAX_BET = 5


class Piece:
    def __init__(self, id: int, text: str, mult: int = 1, wild: bool = False, img: str = ''):
        self.id = id
        self.text = text
        self.multiplier = mult
        self.is_wild = wild
        self.img = img if img else text

    def __repr__(self):
        return self.text

    @property
    def description(self):
        return f'id: {self.id} text: {self.text} mult: {self.multiplier} wild: {self.is_wild}'


default_pieces = [
    Piece(0, '*A*'), Piece(1, '*B*'), Piece(2, '*C*'), Piece(3, '*D*'),
    Piece(4, '*E*'), Piece(5, '*F*'), Piece(6, '*G*', 2), Piece(7, '***', 1, True),
    Piece(8, '*H*'), Piece(9, '*I*'),
]


class Reel:
    def __init__(self, pos: int, pieces: list[Piece], window_height: int, random_offset: int):
        self.pos = pos
        self.pieces = pieces
        self.window_height = window_height

        Reel.rotate(self, random_offset)

    @property
    def visible_rows(self):
        return self.pieces[0:self.window_height]

    @property
    def visible_column_str(self) -> str:
        text = ''
        for p in self.pieces[0:self.window_height]:
            text += p.img
            text += '\n'
        return text

    def rotate(self, cnt=1):
        for i in range(cnt):
            self.pieces.insert(0, self.pieces.pop())

    def __repr__(self) -> str:
        return f'{self.visible_rows}'


# class Reels:
#     def __init__(self):
#         self.reels: list[Reel] = []
#         self.snapshots: list[list[Reel]] = []
#
#     def __repr__(self):
#         return f'{self.reels}'
#
#     def __iter__(self):
#         return iter(self.reels)
#
#     def take_reels_snapshot(self):
#         self.snapshots.append(self.reels)
#
#     @property
#     def resting_reels(self) -> list[Reel]:
#         return self.snapshots[-1]


class Shape:
    def __init__(self, name: str, y_offsets: list, multiplier: int = 3):
        self.name = name
        self.y_offsets = y_offsets
        self.multiplier = multiplier

    @property
    def length(self):
        return len(self.y_offsets)

    @property
    def coordinates(self) -> list[tuple[int, int]]:
        return [(i, self.y_offsets[i]) for i in range(len(self.y_offsets))]

    def __repr__(self):
        return f'{self.name} {self.multiplier} {self.coordinates}'


default_shapes = [
    Shape('Three Reel Straight', [0, 0, 0], 2), Shape('Four Reel Straight', [0, 0, 0, 0], 4),
    Shape('Five Reel Straight', [0, 0, 0, 0, 0], 10), Shape('Lowercase W', [0, 1, 0, 1, 0]),
    Shape('Pyramid', [2, 1, 0, 1, 2]), Shape('Falling Profits', [2, 1, 0, 1, 2]),
    Shape('Uppercase W', [0, 2, 0, 2, 0]), Shape('Rising Profits', [2, 1, 1, 1, 0]),
    Shape('Middle Finger', [2, 2, 0, 2, 2]), Shape('Crown', [1, 2, 0, 2, 1]),
    Shape('Robot Face', [0, 2, 2, 2, 0]), Shape('Reverse REI Logo', [0, 1, 0, 1, 2]),
    Shape('Uppercase M', [2, 0, 2, 0, 2]), Shape('Space Invaders', [1, 0, 0, 0, 1])]


# these are only functional for 5 reels
class PayLine:
    pay_line_id = 0

    def __init__(self, shape: Shape, coordinates: list[tuple[int, int]]):
        self.line_number = PayLine.pay_line_id
        self.shape = shape
        self.coordinates = coordinates
        self.pieces: list[Piece] = []

        PayLine.pay_line_id += 1

    @property
    def default_multiplier(self) -> int:
        return self.shape.multiplier

    @property
    def is_winner(self) -> bool:
        if len(set(self.pieces)) == 1:  # they are all the same
            return True
        if len(set(self.pieces)) == 2 and sum([p.is_wild for p in self.pieces]) > 0:  # all same or a wild
            return True
        return False

    @property
    def winning_multiplier(self) -> int:
        total_piece_multiplier = 1
        for x in [p.multiplier for p in self.pieces]:
            total_piece_multiplier = total_piece_multiplier * x
        return total_piece_multiplier * self.shape.multiplier

    def update_pieces(self, pieces: list[Piece]):
        self.pieces = pieces

    @property
    def winning_pay_line_text(self) -> str:
        return f'Line Number: {self.line_number}; Multiplier: {self.shape.multiplier}; Shape: {self.shape.name};' \
               f'Pieces: {[p.text for p in self.pieces]}'


class PayoutSummary:
    def __init__(self, total: int, line_texts: list[str], new_balance: float):
        self.total = total
        self.line_texts = line_texts
        self.new_balance = new_balance

    # def line_text_cycler(self):
    #     return cycle(self.line_texts)

    @property
    def line_text_w_new_line(self):
        text = ''
        for line_text in self.line_texts:
            text += line_text
            text += '\n'
        return text


class Slots(Game):
    def __init__(self, player_emails: list[str] = [], slots_balance: float = 0):
        super().__init__(game_name='slots', player_emails=player_emails)
        self.state = 'betting'
        self.slots_balance = slots_balance
        self.min_same_line_match = MIN_SAME_LINE_MATCH
        self.max_bet = MAX_BET
        self.pieces: list[Piece] = default_pieces
        self.game_shapes: list[Shape] = default_shapes
        self.pay_lines: list[PayLine] = create_default_paylines()
        self.winning_pay_lines: list[PayLine] = []
        self.reel_cnt = REEL_CNT
        self.reel_len = REEL_LENGTH
        self.spin_bet: int = 0
        self.balance_before_spin: float = 0
        self.rotation_counts = []

        piece_in_cycle = cycle(self.pieces)
        self.reels: list[Reel] = [(Reel(i, [next(piece_in_cycle) for _ in range(self.reel_len + 1)],
                                  REEL_WINDOW_HEIGHT, random.randint(5, 50))) for i in range(self.reel_cnt)]
        self.reels_snapshots: list[list[Reel]] = []

        self.payout_summary: PayoutSummary = PayoutSummary(0, [], self.slots_balance)

    @property
    def as_dictionary(self) -> dict:
        return self.__dict__

    @property
    def game_data_dict(self) -> dict:
        slots.game_end_ts = datetime.utcnow()
        return {'starting_bal': self.balance_before_spin, 'spin_bet': self.spin_bet,
                # 'ending_reels': self.reels_pieces_desc,
                'payout': self.spin_payout, 'ending_bal': slots.slots_balance}

    def send_end_game_data_to_parent(self):
        self.game_data = self.game_data_dict

    @property
    def spun_reels(self):
        return self.reels_snapshots[-1]

    # this needs to be the IDs, not the full pieces

    @property
    def transposed_reels(self):  # this is used during the evaluation of pay_lines
        return [[self.reels[j].pieces[i] for j in range(self.reel_cnt)] for i in range(REEL_WINDOW_HEIGHT)]

    @property
    def reels_pieces_desc(self):
        return [[self.reels[j].pieces[i].description for j in range(self.reel_cnt)] for i in range(REEL_WINDOW_HEIGHT)]

    @property
    def spin_payout(self):
        return sum([pl.winning_multiplier for pl in self.winning_pay_lines])

    def set_rotation_counts(self):
        self.rotation_counts = [random.randint(ROTATIONS[i][0], ROTATIONS[i][1]) for i in range(REEL_CNT)]

    def spin(self, spin_bet: int):
        self.balance_before_spin = self.slots_balance  # does this actually copy it at that point?
        self.spin_bet = spin_bet
        self.slots_balance -= self.spin_bet

        # spin the reels
        slots.state = 'spinning'
        self.set_rotation_counts()
        for i in range(max(self.rotation_counts)):
            for r in self.reels:
                if i <= self.rotation_counts[r.pos]:
                    r.rotate()
            self.reels_snapshots.append(deepcopy(self.reels))
        return

    def check_for_winners(self):
        self.state = 'paying'
        # check for winners
        # probably an odd way to do this. for each pay_line, feed in the actual values and then do the comparison ...
        # ... wholly in the PayLine class
        for pl in self.pay_lines:
            pl.update_pieces([self.transposed_reels[coord[1]][coord[0]] for coord in pl.coordinates])
        self.winning_pay_lines: list[PayLine] = [pl for pl in self.pay_lines if pl.is_winner]
        self.slots_balance += self.spin_payout
        self.payout_summary = PayoutSummary(self.spin_payout,
                                            [pl.winning_pay_line_text for pl in self.winning_pay_lines],
                                            self.slots_balance)

    def end_round(self):
        self.state = 'game_over'
        self.send_end_game_data_to_parent()
        self.update_player_info({'slots_balance': slots.slots_balance})
        self.write_game_to_db()


def create_default_pieces() -> list[Piece]:
    return [Piece(0, '*A*'), Piece(1, '*B*'), Piece(2, '*C*'), Piece(3, '*D*'),
            Piece(4, '*E*'), Piece(5, '*F*'), Piece(6, '*G*', 2), Piece(7, '***', 1, True),
            Piece(8, '*H*'), Piece(9, '*I*')]


def create_default_shapes() -> list[Shape]:
    return [Shape('Three Reel Straight', [0, 0, 0], 2), Shape('Four Reel Straight', [0, 0, 0, 0], 4),
            Shape('Five Reel Straight', [0, 0, 0, 0, 0], 10), Shape('Lowercase W', [0, 1, 0, 1, 0]),
            Shape('Pyramid', [2, 1, 0, 1, 2]), Shape('Falling Profits', [2, 1, 0, 1, 2]),
            Shape('Uppercase W', [0, 2, 0, 2, 0]), Shape('Rising Profits', [2, 1, 1, 1, 0]),
            Shape('Middle Finger', [2, 2, 0, 2, 2]), Shape('Crown', [1, 2, 0, 2, 1]),
            Shape('Robot Face', [0, 2, 2, 2, 0]), Shape('Reverse REI Logo', [0, 1, 0, 1, 2]),
            Shape('Uppercase M', [2, 0, 2, 0, 2]), Shape('Space Invaders', [1, 0, 0, 0, 1])]


def create_default_paylines() -> list[PayLine]:
    list_of_lists = [create_pay_line(s, REEL_WINDOW_HEIGHT) for s in default_shapes]
    return [item for row in list_of_lists for item in row]


# --- customizations that users can make ---

def create_piece(text: str, img: str, mult: int = 1, wild: bool = False) -> Piece:
    piece = Piece(text, img, mult, wild)
    slots.pieces.append(piece)
    return piece


def create_game_shape(name: str, y_offsets: list[int], multiplier: int = 3) -> Shape:
    shape = Shape(name, y_offsets, multiplier)
    slots.game_shapes.append(shape)
    return shape

def create_pay_line(s: Shape, reel_window_height: int) -> list[PayLine]:
    starting_y = 0
    pay_lines: list[PayLine] = []
    while starting_y + max(s.y_offsets) <= reel_window_height - 1:
        pay_lines.append(PayLine(s, [(idx, starting_y + y_offset) for idx, y_offset in enumerate(s.y_offsets)]))
        starting_y += 1
    return pay_lines


slots: Slots

import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import datetime
from ... games_module import Game

REEL_WINDOW_CNT = 5  # need to duplicate this here to avoid a circular import

class Slots(Game):
    game_name = 'slots'

    def __init__(self, player_emails: list[str] = [], slots_balance: float = 0):
        super().__init__(game_name=Slots.game_name, player_emails=player_emails)
        self.state = 'betting'
        self.slots_balance = slots_balance


class Piece:
    def __init__(self, id: int, img: str, mult: int = 1, wild: bool = False):
        self.id = id
        self.img = img
        self.multiplier = mult
        self.is_wild = wild

    def __repr__(self):
        return self.img


class Reel:
    def __init__(self, pos: int, pieces: list[Piece], random_offset: int):
        self.pos = pos
        self.pieces = pieces

        Reel.rotate(self, random_offset)

    def visible_rows(self):
        return self.pieces[0:REEL_WINDOW_CNT]

    def rotate(self, cnt=1):
        for i in range(cnt):
            self.pieces.insert(0, self.pieces.pop())

    def __repr__(self) -> str:
        return f'{self.visible_rows()}'


class Spin:
    def __init__(self, user_email: str, starting_bal: float, bet_amt: int, pay_lines: list):
        self.user_email = user_email
        self.starting_bal = starting_bal
        self.bet_amt = bet_amt
        self.pay_lines = pay_lines
        self.created_ts = datetime.now()
        self.payout = 0
        self.spun_matrix: list[list[Piece]] = []

    def update_payout(self, payout: float):
        self.payout += payout

    def update_matrix(self, m: list[Reel], reel_cnt: int, window_height: int):
        self.spun_matrix = [[m[j].pieces[i] for j in range(reel_cnt)] for i in range(window_height)]

    @property
    def spun_matrix_ids(self) -> list[list[int]]:
        return [[p.id for p in r] for r in self.spun_matrix]


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


# these are only functional for 5 reels
class PayLine:
    def __init__(self, line_number: int, shape: Shape, coordinates: list[tuple[int, int]]):
        self.line_number = line_number
        self.shape = shape
        self.coordinates = coordinates
        self.pieces: list[Piece] = []

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

    def __repr__(self):
        return f'Line Number: {self.line_number}; Multiplier: {self.shape.multiplier}; Shape: {self.shape.name}; Coordinates: {self.coordinates}'

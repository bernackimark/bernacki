import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from dataclasses import dataclass, field
from datetime import date, datetime
import uuid
from copy import copy
from bets.enums import BetStatus, BetTypeEnum, PrivacyLevel, PrizeType


# from db import all_bets


@dataclass
class BetType:
    type: BetTypeEnum
    bet_type_extras: dict = field(default_factory=dict)


@dataclass
class OU(BetType):
    what: str = ''
    line: float = -1
    unit: str = ''
    over_email: str = ''
    under_email: str = ''

    def __post_init__(self):
        self.extras = {'what': self.what, 'line': self.line, 'unit': self.unit, 'over_email': self.over_email,
                       'under_email': self.under_email}


@dataclass
class Prize:
    type: PrizeType
    creator_win_cents: int
    receiver_win_cents: int
    creator_win_other: str
    receiver_win_other: str

    @property
    def creator_win_dollars_cents(self) -> int:
        return int(round(self.creator_win_cents / 100, 0))

    @property
    def receiver_win_dollars_cents(self) -> int:
        return int(round(self.receiver_win_cents / 100, 0))


@dataclass
class Bet:
    creator: str
    receiver: str
    bet_type: BetType
    privacy_level: PrivacyLevel
    prize: Prize
    memo: str
    maturity_dt: date
    id: str = None
    winner: str = None
    created_dt: date = date.today()
    agreement_dt: date = None
    status: BetStatus = BetStatus.PROPOSED
    last_updater: str = None
    lmt: datetime = datetime.now()
    history: list = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.last_updater:
            self.last_updater = self.creator

    def log_to_history(self):
        self.history.append(copy(self))

    def update_lmt_and_modifier(self, current_user):
        self.lmt = datetime.now()
        self.last_updater = current_user

    def rollback_status(self, current_user):
        self.log_to_history()
        self.status = self.history[-2].status
        self.update_lmt_and_modifier(current_user)

    def update_status(self, current_user: str, new_status: BetStatus):
        self.log_to_history()
        self.status = new_status
        self.update_lmt_and_modifier(current_user)

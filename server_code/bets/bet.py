from dataclasses import dataclass, field
from datetime import date, datetime
import uuid
from copy import copy

bet_statuses = ['proposed', 'withdrawn', 'rejected', 'active', 'cancelled', 'pending_outcome',
                'suggested_creator_win', 'suggested_receiver_win', 'suggested_push', 'suggested_cancel',
                'push', 'creator_pending_payment', 'receiver_pending_payment', 'paid', 'complete']
# this seems like a weird mashup of status & role

# from db import all_bets


@dataclass
class BetType:
    type: str = None
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
    type: str
    loss_float: float = None
    loss_str: str = None
    win_float: float = None
    win_str: str = None

    @property
    def loss_dollars_cents(self) -> int:
        return int(round(self.loss_float / 100, 0))

    @property
    def win_dollars_cents(self) -> int:
        return int(round(self.loss_float / 100, 0))


@dataclass
class Party:
    email: str
    prize: Prize
    role: str = 'creator'  # creator/receiver
    memo: str = None
    outcome: str = None
    drinks_level: int = None

    @property
    def is_winner(self) -> bool:
        if self.outcome != 'win':
            return False
        return True

    @property
    def is_loser(self) -> bool:
        if self.outcome == 'loss':
            return True
        return False


@dataclass
class Bet:
    parties: list[Party]
    bet_type: BetType
    title: str  # memo has been renamed as title ... memo is now a personalized concept inside Party
    maturity_dt: date
    id: str = None
    bet_category: str = None
    privacy_level: str = 'private'
    created_dt: date = date.today()
    agreement_dt: date = None
    status: str = 'proposed'
    last_updater: str = None
    lmt: datetime = datetime.now()
    history: list = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.last_updater:
            self.last_updater = self.parties[0].email  # can i guarantee that the creator is the first party?

    def log_to_history(self):
        self.history.append(copy(self))

    def update_lmt_and_modifier(self, current_user):
        self.lmt = datetime.now()
        self.last_updater = current_user

    def rollback_status(self, current_user):
        self.log_to_history()
        self.status = self.history[-2].status
        self.update_lmt_and_modifier(current_user)

    def update_status(self, current_user: str, new_status: str):
        self.log_to_history()
        self.status = new_status
        self.update_lmt_and_modifier(current_user)

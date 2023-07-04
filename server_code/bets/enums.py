import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from enum import StrEnum, auto


class BetStatus(StrEnum):
    PROPOSED = auto()
    WITHDRAWN = auto()
    REJECTED = auto()
    ACTIVE = auto()
    CANCELLED = auto()
    PENDING_OUTCOME = auto()
    SUGGESTED_CREATOR_WIN = auto()
    SUGGESTED_RECEIVER_WIN = auto()
    SUGGESTED_PUSH = auto()
    SUGGESTED_CANCEL = auto()
    PUSH = auto()
    CREATOR_PENDING_PAYMENT = auto()
    RECEIVER_PENDING_PAYMENT = auto()
    PAID = auto()

    def __repr__(self):
        return f'{self.name}'


class PrivacyLevel(StrEnum):
    PRIVATE = auto()
    PUBLIC = auto()
    FRIENDS = auto()

    def __repr__(self):
        return f'{self.name}'


class PrizeType(StrEnum):
    FINANCIAL = auto()
    OTHER = auto()

    def __repr__(self):
        return f'{self.name}'


class BetTypeEnum(StrEnum):
    OU = auto()
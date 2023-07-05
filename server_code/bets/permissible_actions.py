import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

"""
Status	                Current User        Action              New Status
PROPOSED	            Creator	            withdraw	        WITHDRAWN
PROPOSED		                            modify	            PROPOSED
PROPOSED	            Receiver	        reject	            REJECTED
PROPOSED	            last updater	    withdraw	        PROPOSED
ACTIVE		                                suggest_cancel	    SUGGESTED_CANCEL
SUGGESTED_CANCEL	    not last updater	accept_cancel	    CANCELLED
PENDING_OUTCOME		                        suggest_win	        SUGGESTED_CREATOR_WIN
PENDING_OUTCOME		                        suggest_loss	    SUGGESTED_RECEIVER_WIN
PENDING_OUTCOME		                        suggest_push	    SUGGESTED_PUSH
SUGGESTED_CREATOR_WIN	not last updater	confirm_creator_win	CREATOR_PENDING_PAYMENT
SUGGESTED_CREATOR_WIN	not last updater	deny	            PENDING_OUTCOME
SUGGESTED_RECEIVER_WIN	not last updater	confirm_receiver_winRECEIVER_PENDING_PAYMENT
SUGGESTED_RECEIVER_WIN	not last updater	deny	            PENDING_OUTCOME
SUGGESTED_PUSH	        not last updater	confirm_push	    PAID
SUGGESTED_PUSH	        not last updater	deny	            PENDING_OUTCOME
CREATOR_PENDING_PAYMENT	Creator	            confirm_paid	    PAID
RECEIVER_PENDING_PAYMENTReceiver	        confirm_paid	    PAID
"""

# from enum import StrEnum, auto
# from bets.enums import BetStatus


# class Actions(StrEnum):
#     WITHDRAW = auto()
#     MODIFY = auto()
#     REJECT = auto()
#     SUGGEST_CANCEL = auto()
#     ACCEPT_CANCEL = auto()
#     SUGGEST_WIN = auto()
#     SUGGEST_LOSS = auto()
#     SUGGEST_PUSH = auto()
#     DENY = auto()
#     CONFIRM_CREATOR_WIN = auto()
#     CONFIRM_RECEIVER_WIN = auto()
#     CONFIRM_PUSH = auto()
#     CONFIRM_PAID = auto()


# # this is too hard to read & inflexible ... can this be changed into some type of registry?


# def get_perm_actions(current_status: str, user_email: str, creator_email: str,
#                      receiver_email: str, last_updater_email: str) -> list[Actions]:
#     permissible_actions = []
#     if current_status == BetStatus.PROPOSED:
#         permissible_actions.append(Actions.MODIFY)
#         if user_email == creator_email or user_email == last_updater_email:
#             permissible_actions.append(Actions.WITHDRAW)
#         elif user_email == receiver_email:
#             permissible_actions.append(Actions.REJECT)
#     elif current_status == BetStatus.ACTIVE:
#         permissible_actions.append(Actions.SUGGEST_CANCEL)
#     elif current_status == BetStatus.SUGGESTED_CANCEL and user_email != last_updater_email:
#         permissible_actions.append(Actions.ACCEPT_CANCEL)
#     elif current_status == BetStatus.PENDING_OUTCOME:
#         permissible_actions.append(Actions.SUGGEST_WIN)
#         permissible_actions.append(Actions.SUGGEST_LOSS)
#         permissible_actions.append(Actions.SUGGEST_PUSH)
#     elif current_status == BetStatus.SUGGESTED_CREATOR_WIN and user_email != last_updater_email:
#         permissible_actions.append(Actions.CONFIRM_CREATOR_WIN)
#         permissible_actions.append(Actions.DENY)
#     elif current_status == BetStatus.SUGGESTED_RECEIVER_WIN and user_email != last_updater_email:
#         permissible_actions.append(Actions.CONFIRM_RECEIVER_WIN)
#         permissible_actions.append(Actions.DENY)
#     elif current_status == BetStatus.SUGGESTED_PUSH and user_email != last_updater_email:
#         permissible_actions.append(Actions.CONFIRM_PUSH)
#         permissible_actions.append(Actions.DENY)
#     elif current_status == BetStatus.CREATOR_PENDING_PAYMENT and user_email == creator_email:
#         permissible_actions.append(Actions.CONFIRM_PAID)
#     elif current_status == BetStatus.RECEIVER_PENDING_PAYMENT and user_email == receiver_email:
#         permissible_actions.append(Actions.CONFIRM_PAID)
#     else:
#         pass
#     return permissible_actions



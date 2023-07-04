import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from bets.bet import Bet
from db import all_bets
from user import user1, user3
from bets.permissible_actions import Actions, get_perm_actions
from bets.enums import BetStatus

current_user = user1


def get_my_bets(email: str) -> list[Bet]:
    return [Bet(**b) for b in all_bets if email in [b['creator'], b['receiver']]]


my_bets = get_my_bets(current_user.email)


def get_my_actions(bet: Bet, email: str) -> list[Actions]:
    return get_perm_actions(bet.status, email, bet.creator, bet.receiver, bet.last_updater)


# to be a scheduled task
# look at db for any maturity dates in past where status is ACTIVE, set to PENDING_OUTCOME
def update_pending_outcome() -> None:
    raise NotImplementedError

@anvil.server.callable
def write_bets() -> None:
  app_tables.bets_bets.add_row(agreement_dt=date(2023, 4, 2), bet_type={'type': 'OU', 'bet_type_extras': {'what': 'Braves', 'line': 92, 'unit': 'wins', 'over_email': 'jdumond812gmail.com', 'under_email': 'bernackimark@gmail.com'}},
                               created_dt=datetime.now(), creator='bernackimark@gmail.com', history=[], id='abc-123', last_updater='bernackimark@gmail.com', lmt=datetime.now(),
                               maturity_dt=date(2023, 10, 2), memo='Braves OU 92: Jake Over, Bernacki Under', privacy_level='PUBLIC',
                               prize={'type': 'FINANCIAL', 'creator_win_cents': 5000, 'receiver_win_cents': 5000, 'creator_win_other': '', 'receiver_win_other': ''},
                               receiver='jdumond812@gmail.com', status='PROPOSED', winner=None)


all_bets = [{'creator': 'bernackimark@gmail.com', 'receiver': 'jdumond812@gmail.com', 'bet_type': {'type': 'OU', 'bet_type_extras': {'what': 'Braves', 'line': 92, 'unit': 'wins', 'over_email': 'jdumond812gmail.com', 'under_email': 'bernackimark@gmail.com'}},
         'privacy_level': 'PUBLIC', 'prize': {'type': 'FINANCIAL', 'creator_win_cents': 5000, 'receiver_win_cents': 5000, 'creator_win_other': '', 'receiver_win_other': ''},
         'memo': 'Braves OU 92: Jake Over, Bernacki Under', 'maturity_dt': date(2023, 10, 2), 'id': 'abc-123',
             'winner': None, 'created_dt': date(2023, 4, 1), 'agreement_dt': date(2023, 4, 2), 'status': 'PROPOSED', 'last_updater': None, 'lmt': datetime.now(), 'history': []},
            {'creator': 'bernackimark@gmail.com', 'receiver': 'jdumond812@gmail.com', 'bet_type': {'type': 'OU', 'bet_type_extras': {'what': 'Rangers', 'line': 79.5, 'unit': 'wins', 'over_email': 'bernackimark@gmail.com', 'under_email': 'jdumond812@gmail.com'}},
             'privacy_level': 'PUBLIC', 'prize': {'type': 'FINANCIAL', 'creator_win_cents': 5000, 'receiver_win_cents': 5000, 'creator_win_other': '', 'receiver_win_other': ''},
             'memo': 'Rangers OU 79.5: Bernacki Over, Jake Under', 'maturity_dt': date(2023, 10, 2), 'id': 'abc-321',
             'winner': None, 'created_dt': date(2023, 4, 1), 'agreement_dt': date(2023, 4, 2), 'status': 'PROPOSED', 'last_updater': None, 'lmt': datetime.now(), 'history': []},
         ]

this_bet = my_bets[1]
print(0, this_bet.status, this_bet.last_updater, this_bet.lmt, len(this_bet.history))
print()

# Note: When the Bet is returned from the db, I don't think the bet status enum is preserved
# BetStatus.PENDING_OUTCOME is simply a str 'PENDING_OUTCOME'

current_user = user3
print(1, current_user.email, this_bet.status, get_my_actions(this_bet, current_user.email))
this_bet.update_status(current_user.email, BetStatus.SUGGESTED_PUSH)
print(this_bet.status, this_bet.last_updater, this_bet.lmt, len(this_bet.history))
print()

current_user = user1
print(2, current_user.email, this_bet.status, get_my_actions(this_bet, current_user.email))
this_bet.rollback_status(current_user.email)
print(this_bet.status, this_bet.last_updater, this_bet.lmt, len(this_bet.history))
print()

current_user = user1
print(3, current_user.email, this_bet.status, get_my_actions(this_bet, current_user.email))
this_bet.update_status(current_user.email, BetStatus.SUGGESTED_CREATOR_WIN)
print(this_bet.status, this_bet.last_updater, this_bet.lmt, len(this_bet.history))
print()

current_user = user3
print(4, current_user.email, this_bet.status, get_my_actions(this_bet, current_user.email))
this_bet.update_status(current_user.email, BetStatus.CREATOR_PENDING_PAYMENT)
print(this_bet.status, this_bet.last_updater, this_bet.lmt, len(this_bet.history))
print()

current_user = user1
print(5, current_user.email, this_bet.status, get_my_actions(this_bet, current_user.email))
this_bet.update_status(current_user.email, BetStatus.PAID)
print(this_bet.status, this_bet.last_updater, this_bet.lmt, len(this_bet.history))
print()


# todos:
# simplify permissible actions
# implement privacy levels
# if i take the over on the Rangers, I want to see Rangers o79.5 ... but the receiver want a completely diff title
# this is also like the Outcome.  one person may see "win" while the other may see "lose"

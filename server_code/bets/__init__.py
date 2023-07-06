import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from .. import bets_module as m
from datetime import date, datetime
import uuid

# from bets.bet import Bet
# from db import all_bets
# from user import user1, user3
# from bets.permissible_actions import Actions, get_perm_actions
# from bets.enums import BetStatus

from dataclasses import dataclass

@dataclass
class Party:
  name: str = 'John'

@dataclass
class Bet:
  party: Party

@anvil.server.callable
def write_test_bet() -> None:
  bet = Bet(Party())
  app_tables.bets_bets2.add_row(bet=bet)


@anvil.server.callable
def write_bet_single_party(d: dict) -> None:
  app_tables.bets_bets.add_row(
  parties = [{'drinks_level': d['drinks_level'], 'email': d['creator'], 'memo': None, 'prize': None,
            'outcome': {'result': d['outcome'], 'wager_type': d['creator_prize_type'], 'net': d['net']},
            'role': 'creator'}],
  bet_type = {'type': None, 'extras': None},
  title = d['title'], maturity_dt = d['maturity_dt'], id = str(uuid.uuid4()), bet_category = d['bet_category'], privacy_level = 'private',
  created_dt = date.today(), agreement_dt = None, status = 'complete', last_updater = d['creator'], lmt = datetime.now(), history = None
  )
# current_user = user1


# def get_my_bets(email: str) -> list[Bet]:
#     return [Bet(**b) for b in all_bets if email in [b['creator'], b['receiver']]]


# my_bets = get_my_bets(current_user.email)


# def get_my_actions(bet: Bet, email: str) -> list[Actions]:
#     return get_perm_actions(bet.status, email, bet.creator, bet.receiver, bet.last_updater)


# to be a scheduled task
# look at db for any maturity dates in past where status is ACTIVE, set to PENDING_OUTCOME
def update_pending_outcome() -> None:
    raise NotImplementedError

@anvil.server.callable
def write_bets() -> None:
  app_tables.bets_bets.add_row(agreement_dt=date(2023, 4, 2), bet_type={'type': 'OU', 'bet_type_extras': {'what': 'Braves', 'line': 92, 'unit': 'wins', 'over_email': 'jdumond812gmail.com', 'under_email': 'bernackimark@gmail.com'}},
                               created_dt=date.today(), creator='bernackimark@gmail.com', history=[], id='abc-123', last_updater='bernackimark@gmail.com', lmt=datetime.now(),
                               maturity_dt=date(2023, 10, 2), memo='Braves OU 92: Jake Over, Bernacki Under', privacy_level='Public',
                               creator_prize={'prize_type': 'Financial', 'to_win': 50}, receiver_prize={'prize_type': 'Other', 'to_win': 'A case of Natty Light'},
                               receiver='jdumond812@gmail.com', status='Proposed', winner=None)
  for r in app_tables.bets_bets.search():
    print(dict(r))

@anvil.server.callable
def print_incoming_data(data) -> None:
  print(data)

# todos:
# simplify permissible actions
# implement privacy levels
# if i take the over on the Rangers, I want to see Rangers o79.5 ... but the receiver want a completely diff title
# this is also like the Outcome.  one person may see "win" while the other may see "lose"

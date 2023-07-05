import anvil.server
from datetime import date, datetime

users = [('Mark Bernacki', 'bernackimark@gmail.com'), ('Jake Dumond', 'jdumond812@gmail.com')]
bet_types = [('OU', 'OU')]
privacy_levels = [('Friends', 'Friends'), ('Public', 'Public'), ('Private', 'Private')]
prize_types = [('Financial', 'Financial'), ('Other', 'Other')]

def get_all_other_users(current_user_email: str) -> list[str]:
  return [u for u in users if u[1] != current_user_email]

def auto_generate_new_bet_title(ui_data: list[dict], bet_type: str) -> str:
  print(ui_data)
  # flatten the incoming list of dicts
  d = {k: v for d in ui_data for k, v in d.items()}
  if bet_type == 'OU':
    return f"{d['what']} over/under {d['line']} {d['units']}"

@anvil.server.portable_class
class Bet():
    def __init__(self, creator: str, receiver: str, bet_type: dict, privacy_level: str, creator_prize_type: str, creator_to_win: str,
                 receiver_prize_type: str, receiver_to_win: str, memo: str, maturity_dt: date):
      self.creator = creator
      self.receiver = receiver
      self.bet_type = bet_type
      self.privacy_level = privacy_level
      self.creator_prize = {'prize_type': creator_prize_type, 'to_win': creator_to_win}
      self.receiver_prize = {'prize_type': receiver_prize_type, 'to_win': receiver_to_win}
      self.memo = memo
      self.maturity_dt = maturity_dt

      if self.creator_prize['prize_type'] == 'Financial':
        self.creator_prize['to_win'] = float(self.creator_prize['to_win'])
      if self.receiver_prize['prize_type'] == 'Financial':
        self.receiver_prize['to_win'] = float(self.receiver_prize['to_win'])

# the_bet = Bet(creator='bernackimark@gmail.com', receiver='jdumond812@gmail.com',
#     bet_type={'type': 'OU', 'bet_type_extras': {'what': 'Red Sox', 'line': 76.5, 'unit': 'wins', 'over_email': 'bernackimark@gmail.com', 'under_email': 'jdumond812@gmail.com'}},
#     privacy_level='Public', prize={'type': 'FINANCIAL', 'creator_win_cents': 5000, 'receiver_win_cents': 5000, 'creator_win_other': '', 'receiver_win_other': ''},
#     memo='Red Sox OU 76.5, Bernacki Over, Jake Under', maturity_dt=date(2023, 10, 2))

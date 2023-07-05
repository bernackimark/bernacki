import anvil.server
from datetime import date, datetime

users = [('Mark Bernacki', 'bernackimark@gmail.com'), ('Jake Dumond', 'jdumond812@gmail.com')]
bet_types = [('OU', 'OU')]
outcomes = [('Win', 'win'), ('Loss', 'loss'), ('Push', 'push')]
privacy_levels = [('Friends', 'Friends'), ('Public', 'Public'), ('Private', 'Private')]
prize_types = [('Financial', 'Financial'), ('Other', 'Other')]
bet_cats = ['Blackjack', 'Poker', 'Roulette', 'Baccarat', 'Craps', 'Keno', 'Video Poker', 'Three Card Poker', 'Pai Gow',
            'Pai Gow Poker', 'Texas Hold\'em (Limit)', 'Daily Fantasy', 'Fantasy Baseball', 'Fantasy Basketball', 'Fantasy Football',
 'March Madness', 'Sic Bo', 'Spanish 21', 'Ultimate Texas Hold\'em', 'Carribean Stud', 'Let It Ride', 'Golf',
 'Other Sports', 'Other', 'Physical Challenge', 'Texas Hold\'em (No Limit)']
bet_categories = [(c, c) for c in sorted(set(bet_cats))]

current_user = {'first': 'Mark', 'last': 'Bernacki', 'full': 'Mark Bernacki', 'email': 'bernackimark@gmail.com'}

def get_all_other_users(current_user_email: str) -> list[str]:
  return [u for u in users if u[1] != current_user_email]

def auto_generate_new_bet_title(ui_data: dict, bet_type: str) -> str:
  if bet_type == 'OU':
    return f"{ui_data['what']} over/under {ui_data['line']} {ui_data['units']}"

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

@anvil.server.portable_class
class SelfBet():
    def __init__(self, creator: str, bet_category: str, prize_type: str, net, memo: str, maturity_dt: date, drinks_level: int, outcome: str):
      self.creator = creator
      self.bet_category = bet_category
      self.privacy_level = 'PRIVATE'
      self.prize = {'prize_type': prize_type, 'to_win': net}
      self.memo = memo
      self.maturity_date = maturity_dt
      self.drinks_levels = drinks_level
      self.outcome = outcome

      if self.prize['prize_type'] == 'Financial':
        self.prize['to_win'] = float(self.creator_prize['to_win'])
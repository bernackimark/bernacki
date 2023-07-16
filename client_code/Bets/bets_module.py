import anvil.server
from datetime import date, datetime

users = [('Mark Bernacki', 'bernackimark@gmail.com'), ('Jake Dumond', 'jdumond812@gmail.com')]
bet_types = [('OU', 'OU')]
outcomes = [('Win', 'win'), ('Loss', 'loss'), ('Push', 'push')]
privacy_levels = [('Friends', 'friends'), ('Public', 'public'), ('Private', 'private')]
prize_types = [('Financial', 'financial'), ('Other', 'other')]
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

      # if self.creator_prize['prize_type'] == 'Financial':
      #   self.creator_prize['to_win'] = float(self.creator_prize['to_win'])
      # if self.receiver_prize['prize_type'] == 'Financial':
      #   self.receiver_prize['to_win'] = float(self.receiver_prize['to_win'])
from ._anvil_designer import ProposeBetTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import bets_module as m

current_user = {'first': 'Mark', 'last': 'Bernacki', 'full': 'Mark Bernacki', 'email': 'bernackimark@gmail.com'}


class ProposeBet(ProposeBetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dd_receiver.items = m.get_all_other_users('bernackimark@gmail.com')
    self.dd_bet_type.items = m.bet_types
    self.dd_privacy_level.items = m.privacy_levels
    self.dd_creator_prize_type.items = self.dd_receiver_prize_type.items = m.prize_types
    self.dd_creator_prize_type.include_placeholder = self.dd_receiver_prize_type.include_placeholder = True
    self.dd_bet_type.include_placeholder = self.dd_receiver.include_placeholder = True
    self.tb_title.placeholder = 'Leave blank for an autogenerated title'
    self.dd_receiver.tag = 'receiver_name'
    self.dd_bet_type.tag = 'bet_type'


  def dd_bet_type_change(self, **event_args):
    if self.dd_bet_type.selected_value == 'OU':
      tb_what = TextBox(placeholder='Braves', tag='what')
      tb_line = TextBox(type='number', placeholder=92, tag='line')
      tb_units = TextBox(placeholder='2023 Wins', tag='units')
      lbl_over = Label(text="Who's taking the over?", font_size=16)
      dd_over = DropDown(include_placeholder=True, items=m.users, tag='over_user')
      dd_under = DropDown(include_placeholder=True, placeholder='Under User',items=m.users, tag='under_user')
      self.gp_bet_type_extras.add_component(tb_what, row='A', col_xs=0, width_xs=4)
      self.gp_bet_type_extras.add_component(tb_line, row='A', col_xs=4, width_xs=4)
      self.gp_bet_type_extras.add_component(tb_units, row='A', col_xs=8, width_xs=4)
      self.gp_bet_type_extras.add_component(lbl_over, row='B', col_xs=0, width_xs=3)
      self.gp_bet_type_extras.add_component(dd_over, row='B', col_xs=3, width_xs=9)
    else:
      self.gp_bet_type_extras.clear()

  def dd_creator_prize_type_change(self, **event_args):
    if self.dd_creator_prize_type.selected_value == 'Financial':
      self.tb_creator_winnings = TextBox(placeholder=20.00, type='number')
    else:
      self.tb_creator_winnings = TextBox(placeholder='A case of Natty Light', type='text')
    self.cp_creator_prize.clear()
    self.cp_creator_prize.add_component(self.tb_creator_winnings)

  def dd_receiver_prize_type_change(self, **event_args):
    if self.dd_receiver_prize_type.selected_value == 'Financial':
      self.tb_receiver_winnings = TextBox(placeholder=20.00, type='number')
    else:
      self.tb_receiver_winnings = TextBox(placeholder='A case of Natty Light', type='text')
    self.cp_reciver_prize.clear()
    self.cp_reciver_prize.add_component(self.tb_receiver_winnings)
  
  def btn_propose_bet_click(self, **event_args):
    all_bet_type_extra_values: list[dict] = []
    for c in self.gp_bet_type_extras.get_components():
      if type(c) is TextBox and c.tag:
        all_bet_type_extra_values.append({c.tag: c.text})
      elif type(c) is DatePicker and c.tag:
        all_bet_type_extra_values.append({c.tag: c.date})
      elif type(c) is DropDown and c.tag:
        all_bet_type_extra_values.append({c.tag: c.selected_value}) 
    bet_type_extra_value_dict: dict = {k: v for d in all_bet_type_extra_values for k, v in d.items()}
    if not self.tb_title.text:
      self.tb_title.text = m.auto_generate_new_bet_title(bet_type_extra_value_dict, self.dd_bet_type.selected_value)
    for o in self.card_propose_bet.get_components():
      if (type(o) is TextBox and not o.text) or (type(o) is DatePicker and not o.date) or (type(o) is DropDown and not o.selected_value):
        alert('You missed some data')
        break
    
    data = m.Bet(creator=current_user['email'], receiver=self.dd_receiver.selected_value, 
                 bet_type={'bet_type': self.dd_bet_type.selected_value, 'bet_type_extras': bet_type_extra_value_dict},
                 privacy_level=self.dd_privacy_level.selected_value, creator_prize_type=self.dd_creator_prize_type.selected_value,
                 creator_to_win=self.tb_creator_winnings.text, receiver_prize_type=self.dd_receiver_prize_type.selected_value,
                 receiver_to_win=self.tb_receiver_winnings.text, memo=self.tb_title.text, maturity_dt = self.dp_maturity_dt.date)
    anvil.server.call('print_incoming_data', data)
    
    
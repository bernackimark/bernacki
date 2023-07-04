from ._anvil_designer import BetsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import bets_module as m


class Bets(BetsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dd_receiver.items = m.users
    self.dd_bet_type.items = m.bet_types
    self.dd_privacy_level.items = m.privacy_levels
    self.dd_creator_prize_type.items = self.dd_receiver_prize_type.items = m.prize_types
    self.dd_creator_prize_type.include_placeholder = self.dd_receiver_prize_type.include_placeholder = True
    self.dd_bet_type.include_placeholder = self.dd_receiver.include_placeholder = True


  def dd_bet_type_change(self, **event_args):
    if self.dd_bet_type.selected_value == 'OU':
      tb_what = TextBox(placeholder='Braves')
      tb_line = TextBox(type='number', placeholder=92)
      tb_units = TextBox(placeholder='2023 Wins')
      lbl_over = Label(text="Who's taking the over?", font_size=16)
      dd_over = DropDown(include_placeholder=True, items=m.users)
      dd_under = DropDown(include_placeholder=True, placeholder='Under User',items=m.users)
      # self.cp_bet_type_extras.add_component(tb_what)
      # self.cp_bet_type_extras.add_component(tb_line)
      # self.cp_bet_type_extras.add_component(tb_units)
      # self.cp_bet_type_extras.add_component(dd_over)
      # self.cp_bet_type_extras.add_component(dd_under)
      self.gp_bet_type_extras.add_component(tb_what, row='A', col_xs=0, width_xs=4)
      self.gp_bet_type_extras.add_component(tb_line, row='A', col_xs=4, width_xs=4)
      self.gp_bet_type_extras.add_component(tb_units, row='A', col_xs=8, width_xs=4)
      self.gp_bet_type_extras.add_component(lbl_over, row='B', col_xs=0, width_xs=3)
      self.gp_bet_type_extras.add_component(dd_over, row='B', col_xs=3, width_xs=9)

  def dd_prize_type_change(self, **event_args):
    tb_creator_win_amt = TextBox(placeholder=20.00, type='number')
    tb_receiver_win_amt = TextBox(placeholder=20.00, type='number')
    tb_creator_win_str = TextBox(placeholder='A case of Natty Light')
    tb_receiver_win_str = TextBox(placeholder='Wear a Hello Kitty armband for a week.')

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
    data = m.Bet(creator='bernackimark@gmail.com', receiver=self.dd_receiver.selected_value, bet_type=self.dd_bet_type.selected_value,
                 privacy_level=self.dd_privacy_level.selected_value, creator_prize_type=self.dd_creator_prize_type.selected_value,
                 creator_to_win=self.tb_creator_winnings.text, receiver_prize_type=self.dd_receiver_prize_type.selected_value,
                 receiver_to_win=self.tb_receiver_winnings.text, memo=self.tb_title.text, maturity_dt = self.dp_maturity_dt.date)
    print(data)







    
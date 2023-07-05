from ._anvil_designer import SelfBetTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import bets_module as m

from datetime import date

class SelfBet(SelfBetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dp_self_bet.date = date.today()
    self.dd_self_bet_category.include_placeholder = True
    self.dd_self_bet_category.items = m.bet_categories

    # Any code you write here will run before the form opens.

  def btn_self_bet_save_click(self, **event_args):
    data = m.SelfBet(creator=m.current_user['email'], bet_category=self.dd_self_bet_category.selected_value,
                     prize_type = '', net=self.tb_self_bet_net.text, memo=self.tb_self_bet_title.text, maturity_dt=self.dp_self_bet.date,
                     drinks_level = '', outcome = '')

    # need to create the "only one button can be selected concept, and getting the datatype correct for 'net' based on Financial/Other button selected"
    
    anvil.server.call('print_incoming_data', data)


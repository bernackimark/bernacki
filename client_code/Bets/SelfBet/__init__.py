from ._anvil_designer import SelfBetTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import date, datetime
from .. import bets_module as m

class SelfBet(SelfBetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dp_self_bet.date = date.today()
    self.dd_self_bet_category.include_placeholder = True
    self.dd_self_bet_category.items = m.bet_categories

    # Any code you write here will run before the form opens.

  def btn_self_bet_save_click(self, **event_args):
    data = {'creator': m.current_user['email'], 'bet_category': self.dd_self_bet_category.selected_value, 
            'net': self.tb_self_bet_net.text, 'title': self.tb_self_bet_title.text, 'maturity_dt': self.dp_self_bet.date, 
            'outcome': 'win', 'creator_prize_type': 'financial', 'drinks_level': 0}

    # need to create the "only one button can be selected concept, and getting the datatype correct for 'net' based on Financial/Other button selected"
    
    anvil.server.call('write_bet_single_party', data)


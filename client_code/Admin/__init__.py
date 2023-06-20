from ._anvil_designer import AdminTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import dg_module as dgm

class Admin(AdminTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.dd_governing_body.items = dgm.filter_sort_unique_column('governing_body')
    self.dd_designation.items = dgm.filter_sort_unique_column('designation')
    self.get_most_recent_loaded_event()

    winners = {w['mpo_champion'] for w in app_tables.dg_events.search()}
    self.lbl_winners.text = winners

  def get_most_recent_loaded_event(self):
    last_event, last_added_ts = anvil.server.call('get_most_recent_event')
    self.lbl_last_event_added.text = f'Last Event Added: {last_event} on {last_added_ts}' 

  def btn_add_new_dg_event_click(self, **event_args):
    for o in self.card_add_new_dg_event.get_components():
      if (type(o) is TextBox and not o.text) or (type(o) is DatePicker and not o.date) or (type(o) is DropDown and not o.selected_value):
        alert('You missed some data')
        break
    anvil.server.call('write_dg_event', year=self.tb_year.text, governing_body=self.dd_governing_body.selected_value,
                      designation=self.dd_designation.selected_value, start_date=self.dp_start.date, end_date=self.dp_end.date,
                      city=self.tb_city.text, state=self.tb_state.text, country=self.tb_country.text,
                      mpo_champion=self.tb_mpo_champion.text, fpo_champion=self.tb_fpo_champion.text, name=self.tb_name.text)
    self.get_most_recent_loaded_event()

  def btn_clear_click(self, **event_args):
    for o in self.card_add_new_dg_event.get_components():
      if type(o) is TextBox:
        o.text = None
      elif type(o) is DatePicker:
        o.date = None
      elif type(o) is DropDown:
        o.selected_value = None



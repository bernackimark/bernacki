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
    dgm.dg_events = [_ for _ in app_tables.dg_events.search()]
    self.get_most_recent_loaded_event()

  def get_most_recent_loaded_event(self):
    last_event, last_added_ts = anvil.server.call('get_most_recent_event')
    self.lbl_last_event_added.text = f'Last Event Added: {last_event} on:{chr(10)}{last_added_ts:%m.%d.%Y %H:%M:%S}' 

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

  def btn_save_new_golfer_click(self, **event_args):
    for o in self.card_add_new_golfer.get_components():
      if (type(o) is TextBox and not o.text) or (type(o) is DatePicker and not o.date) or (type(o) is DropDown and not o.selected_value):
        alert('You missed some data')
        break
    anvil.server.call('write_disc_golfer', pdga_id=self.tb_pdga_id.text, first_name=self.tb_first_name.text,
                      last_name=self.tb_last_name.text, division=self.dd_division.selected_value)

  def btn_clear_new_golfer_click(self, **event_args):
    for o in self.card_add_new_golfer.get_components():
      if type(o) is TextBox:
        o.text = None
      elif type(o) is DatePicker:
        o.date = None
      elif type(o) is DropDown:
        o.selected_value = None

  def run_geo_btn_click(self, **event_args):
    incoming_data = [{'name': '77 Forest St, New Britain, CT', 'orig': True, 'dest': False, 'lat_long': ()},
                 {'name': 'Taino Prime, Meriden, CT', 'orig': False, 'dest': False, 'lat_long': (40.74844, -73.98566)},
                 {'name': 'New Britain Stadium, New Britain, CT', 'orig': False, 'dest': False, 'lat_long': ()},
                 {'name': '20 Church St, Hartford, CT', 'orig': False, 'dest': True, 'lat_long': ()}]
    anvil.server.call('run_geo', incoming_data)

  def run_geo_no_api_calls_btn_click(self, **event_args):
    incoming_data = [{'name': '77 Forest St, New Britain, CT', 'orig': True, 'dest': False, 'lat_long': ()},
                 {'name': 'Taino Prime, Meriden, CT', 'orig': False, 'dest': False, 'lat_long': (40.74844, -73.98566)},
                 {'name': 'New Britain Stadium, New Britain, CT', 'orig': False, 'dest': False, 'lat_long': ()},
                 {'name': '20 Church St, Hartford, CT', 'orig': False, 'dest': True, 'lat_long': ()}]
    anvil.server.call('run_geo_no_api_calls', incoming_data)

  def btn_known_points_add_click(self, **event_args):
    anvil.server.call('known_points_create')


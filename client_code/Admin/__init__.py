from ._anvil_designer import AdminTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..user import user

class Admin(AdminTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.dd_security.items = [('Admin', 'admin'), ('Private', 'private') , ('Public', 'public'), ('Testing', 'testing')]

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

  # def button_1_click(self, **event_args):
  #   anvil.server.call('run_baseball_bets')

  def btn_run_bets_click(self, **event_args):
    anvil.server.call('write_bets')

  def btn_write_test_bet_click(self, **event_args):
    anvil.server.call('write_test_bet')

  def btn_add_new_app_click(self, **event_args):
    if not self.tb_new_app_name.text or not self.tb_new_app_title.text:
      alert('Enter a name and title, dumbass')
      return
    anvil.server.call_s('write_new_app', name=self.tb_new_app_name.text, title=self.tb_new_app_title.text,
                        group=self.tb_new_app_group.text,
                        user=user.user, icon_str=self.tb_icon_str.text, security=self.dd_security.selected_value)

  def btn_run_mohegan_click(self, **event_args):
    anvil.server.call('run_mohegan_scrape')

  def btn_update_app_click(self, **event_args):
    anvil.server.call('update_app', self.tb_app_name.text, self.tb_key.text, self.tb_value.text)

  def btn_save_new_tourney_name_click(self, **event_args):
    anvil.server.call('write_new_tourney_name', self.tb_new_tourney_name.text)




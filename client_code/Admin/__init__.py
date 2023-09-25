from ._anvil_designer import AdminTemplate
from anvil import *
import anvil.facebook.auth
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

  def btn_run_mohegan_click(self, **event_args):
    anvil.server.call('run_mohegan_scrape')


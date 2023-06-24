from ._anvil_designer import TripBuilderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TripBuilder(TripBuilderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.rp_build_trip.items = [{'name': '77 Forest St, New Britain, CT', 'orig': True, 'dest': False},
                 {'name': 'Taino Prime, Meriden, CT', 'orig': False, 'dest': False},
                 {'name': 'New Britain Stadium, New Britain, CT', 'orig': False, 'dest': False},
                 {'name': '20 Church St, Hartford, CT', 'orig': False, 'dest': True}]
    # Any code you write here will run before the form opens.

  def btn_build_trip_click(self, **event_args):
    for row in self.rp_build_trip.items:
      if row['name'] in ('', None):
        alert('Please enter a location into each row')
        return
    if sum([r['orig'] for r in self.rp_build_trip.items]) != 1 or sum([r['dest'] for r in self.rp_build_trip.items]) != 1:
      alert('Please check exactly one box for origin and destination')
      return
    if [idx for idx, r in enumerate(self.rp_build_trip.items) if r['orig']][0] == [idx for idx, r in enumerate(self.rp_build_trip.items) if r['dest']][0]:
      alert('Please have a different origin & destination.  It is currently a Beta limitation.')
      return
    
    res = anvil.server.call('run_geo', self.rp_build_trip.items)
    self.display_my_routes(res)

  def display_my_routes(self, data: list[dict]):
    self.rp_my_routes.items = sorted(data, key=lambda x: x['duration'])


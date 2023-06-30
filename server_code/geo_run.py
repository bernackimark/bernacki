import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import geography

# incoming_data = [{'name': '77 Forest St, New Britain, CT', 'orig': True, 'dest': False},
#                  {'name': 'Taino Prime, Meriden, CT', 'orig': False, 'dest': False},
#                  {'name': 'New Britain Stadium, New Britain, CT', 'orig': False, 'dest': False},
#                  {'name': '20 Church St, Hartford, CT', 'orig': False, 'dest': True}]

@anvil.server.callable
def run_geo(incoming_data):
  results = geography.run_geography(incoming_data)
  return results
  # print(results)

@anvil.server.callable
def run_geo_no_api_calls(incoming_data):
  results = geography.run_geography_no_api_calls(incoming_data)
  return results
  # print(results)
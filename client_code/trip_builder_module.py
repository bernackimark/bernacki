import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

trip_builder_items: list[dict] = [{'name': '', 'orig': True, 'dest': False},
                 {'name': '', 'orig': False, 'dest': False},
                 {'name': '', 'orig': False, 'dest': False},
                 {'name': '', 'orig': False, 'dest': True}]

def add_item():
  trip_builder_items.append({'name': '', 'orig': False, 'dest': False})
  print(trip_builder_items)

def delete_item(item):
  trip_builder_items.remove(item)
  print(trip_builder_items)

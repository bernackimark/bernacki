import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def get_stuff_details():
  return app_tables.stuff.client_readable()

@anvil.server.callable
def get_stuff_lmt(id_name):
  return app_tables.stuff.get(id_name=id_name)['lmt']



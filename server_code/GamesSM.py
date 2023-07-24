import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from dataclasses import dataclass, field
from datetime import datetime

@anvil.server.callable
def write_game_data(d: dict):
  print('I received the info from the client here on the server')
  print(d)
  app_tables.games_log.add_row(id=len(app_tables.games_log.search())+1, **d)
  
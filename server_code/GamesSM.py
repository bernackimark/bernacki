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
def write_game_data(d: dict, updated_player_data=dict()):
  if updated_player_data:
    user_email = d['player_emails'][0]
    user_row = app_tables.users.get(email=user_email)
    user_row_info: dict = user_row['info']
    for k, v in updated_player_data.items():
      if k in user_row_info.keys():
          user_row_info[k] = v
    user_row['info'] = user_row_info

  # here is the reasoning behind this seemingly odd approach above
  # row = app_tables.my_table.search()[0]
  # dic = row['column_with_dict']
  # dic['key'] = new_value  # row is not aware of this change
  # row['column_with_dict'] = dic  # row is finally updated

  # remove any extra columns before writing a row to the games_log table
  db_columns = [d['name'] for d in app_tables.games_log.list_columns()]
  key_copy = tuple(d.keys())  
  for k in key_copy:
      if k not in db_columns:
          del d[k]
  
  app_tables.games_log.add_row(id=len(app_tables.games_log.search())+1, **d)

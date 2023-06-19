import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def write_game_data(d):
  game_name, game_start_ts, game_end_ts, player_emails = d['app'], d['start_time'], d['end_time'], d['email']
  del d['app'], d['start_time'], d['end_time'], d['email']
  # i need to do that because anvil can't store datetimes in a simple object column
  app_tables.games_log.add_row(id=len(app_tables.games_log.search())+1,
                               game_name=game_name, game_start_ts=game_start_ts, game_end_ts=game_end_ts, player_emails=player_emails,
                               game_data=d)
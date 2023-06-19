import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import date, datetime

def convert_dict_ts_to_isoformat(d: dict) -> dict:
  new_dict = d.copy()
  for v in new_dict.values():
    if isinstance(v, datetime) or isinstance(v, date):
      v = v.isoformat()
  return new_dict

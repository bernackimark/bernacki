import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

import xlrd
import openpyxl
import pandas as pd
from datetime import date, datetime

@anvil.server.callable
def load_spreadsheet(file) -> None:
  with anvil.media.TempFile(file) as f:
    if file.content_type == 'text/csv':
      df = pd.read_csv(f, header=None)
    else:
      df = pd.read_excel(f, header=None)
  write_records(df.to_dict('records'))

def write_records(list_of_dicts: list[dict]):
  for d in list_of_dicts:
    app_tables.dg_events.add_row(city=d[6], country=d[8], 
                                 created_ts=datetime.now(), designation=d[2], end_date=d[4].date(),
                                 fpo_champion=d[10], governing_body=d[1],
                                 id=len(app_tables.dg_events.search())+1,
                                 lmt=datetime.now(), mpo_champion=d[9], name=d[5] , start_date=d[3].date(),
                                 state=d[7], year=d[0])

@anvil.server.callable
def write_dg_event(**kwargs):
  app_tables.dg_events.add_row(id=len(app_tables.dg_events.search())+1, created_ts=datetime.now(), lmt=datetime.now(), **kwargs)

@anvil.server.callable
def get_most_recent_event() -> tuple[str, datetime]:
  return [(r['name'], r['created_ts']) for r in app_tables.dg_events.search(tables.order_by('end_date', ascending=False))][0]

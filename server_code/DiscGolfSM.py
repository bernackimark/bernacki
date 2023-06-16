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




# event_year	governing_body	designation	event_state_date	event_end_date	event_name	event_city	event_state	event_country	mpo_champion	fpo_champion

# {0: 2016, 1: 'DGPT', 2: 'DGPT Undesignated', 3: Timestamp('2016-06-23 00:00:00'), 4: datetime.datetime(2016, 6, 26, 0, 0), 5: 'Vibram Open', 6: 'Leicester', 7: 'MA', 8: 'USA', 9: 'Bradley Williams', 10: 'Paige Pierce'}
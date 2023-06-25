import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import utils

from datetime import date, timedelta

dg_events = []  # [_ for _ in app_tables.dg_events.search()]  I'm now loading this from the Form intializer
leaderboard_groupers = [('MPO Winner', 'mpo_champion'), ('FPO Winner', 'fpo_champion'), ('Event', 'name'), ('Year', 'year')]

def sort_dg_events(column_name, reverse=False):
  return sorted(dg_events, key=lambda x: x[column_name], reverse=reverse)

def filter_sort_unique_column(column_name, reverse=False):
  column = {r[column_name] for r in dg_events if r[column_name] is not None}
  return sorted(column, key=lambda x: x[0], reverse=reverse)

def filter_sort_by_date_desc(column_name, value):
  filtered = [e for e in dg_events if e[column_name] == value]
  return sorted(filtered, key=lambda x: x['end_date'], reverse=True)

def filter_by_time_period(time_period_id):
  time_period = [tp for tp in utils.time_period_begin_end_list if tp[0] == time_period_id][0]
  begin, end = time_period[1], time_period[2]
  filtered = [e for e in dg_events if begin <= e['end_date'] <= end]
  return sorted(filtered, key=lambda x: x['end_date'], reverse=True)

def group_sort_by_column(records: list[dict], grouper_column, reverse=True) -> list[dict]:
  unique_values = {r[grouper_column] for r in records if r[grouper_column] is not None}
  all_values = [r[grouper_column] for r in records if r[grouper_column] is not None]
  list_of_dicts = [{'value': v, 'count': all_values.count(v)} for v in unique_values]
  return sorted(list_of_dicts, key=lambda x: [x['count'], x['value']], reverse=reverse)
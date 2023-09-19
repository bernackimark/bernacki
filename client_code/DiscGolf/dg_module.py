import anvil.server
from datetime import date, timedelta

from .. import utils

dg_data = []  # I'm now loading this from the Form intializer, so that it doesn't run upon App startup
leaderboard_groupers = [('MPO Winner', 'mpo_champion'), ('FPO Winner', 'fpo_champion'), ('Event', 'name'), ('Year', 'year')]

def get_dg_data() -> list[dict]:
    dg_data = []
    for r in anvil.server.call('get_dg_data'):
        event: dict = {'year': r['year'], 'governing_body': r['governing_body'], 'designation': r['designation'],
                      'end_date': r['end_date'], 'created_ts': r['created_ts'], 'name': r['tourney_link']['name'],
                      'city': r['tourney_link']['city'], 'state': r['tourney_link']['state'], 'country': r['tourney_link']['country']}
        if r['mpo_champ_link']:
            event['mpo_champion'] = r['mpo_champ_link']['full_name']
        if r['fpo_champ_link']:
            event['fpo_champion'] = r['fpo_champ_link']['full_name']
        dg_data.append(event)
    return dg_data

def sort_dg_data(column_name, reverse=False):
  return sorted(dg_data, key=lambda x: x[column_name], reverse=reverse)

def filter_sort_unique_column(column_name, reverse=False):
  column = {r[column_name] for r in dg_data if r[column_name] is not None}
  return sorted(column, key=lambda x: x[0], reverse=reverse)

def filter_sort_by_date_desc(column_name, value):
  filtered = [e for e in dg_data if e[column_name] == value]
  return sorted(filtered, key=lambda x: x['end_date'], reverse=True)

def filter_by_time_period(time_period_id):
  time_period = [tp for tp in utils.time_period_begin_end_list if tp[0] == time_period_id][0]
  begin, end = time_period[1], time_period[2]
  filtered = [e for e in dg_data if begin <= e['end_date'] <= end]
  return sorted(filtered, key=lambda x: x['end_date'], reverse=True)

def group_sort_by_column(records: list[dict], grouper_column, reverse=True) -> list[dict]:
  unique_values = {r[grouper_column] for r in records if r[grouper_column] is not None}
  all_values = [r[grouper_column] for r in records if r[grouper_column] is not None]
  list_of_dicts = [{'value': v, 'count': all_values.count(v)} for v in unique_values]
  return sorted(list_of_dicts, key=lambda x: [x['count'], x['value']], reverse=reverse)

def get_image_url_from_name(scoreboard_value: str) -> str:
  # i need this because, the table isn't always displaying a name
  for p in dg_data:
    if p['mpo_champion'] == scoreboard_value or p['fpo_champion'] == scoreboard_value:
      return p['photo_url']
  return ''

def get_tourney_names_from_id(id: int) -> dict:
    return [t for t in dg_event_names if t['id'] == id][0]

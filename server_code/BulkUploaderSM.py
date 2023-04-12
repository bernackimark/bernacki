import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import pandas as pd

from bulk_updater_module import StatusMessage

expected_column_cnt = {1: 2, 2: 2}

@anvil.server.callable
def is_data_valid(file, task_id: int) -> StatusMessage:
  with anvil.media.TempFile(file) as f:
      if file.content_type == 'text/csv':
          df = pd.read_csv(f, header=None)
      else:
          df = pd.read_excel(f, header=None)

  if df.shape[1] != expected_column_cnt[task_id]:
    return StatusMessage(False, f'Your spreadsheet does not have exactly {expected_column_cnt[task_id]} columns of data.')

  sheet = clean_and_convert(df)

  if task_id == 1:
    status_message = is_valid_for_status(sheet)
  elif task_id == 2:
    status_message = is_valid_for_ownership(sheet)

  return status_message

def clean_and_convert(df: pd.DataFrame) -> list[dict]:
  df.columns = ['item_id', 'new_value']
  df.dropna(how='any', inplace=True)
  df.drop_duplicates(keep='first', inplace=True)
  convert_dtype_dict = {'item_id': int, 'new_value': str}
  df.astype(convert_dtype_dict)
  return df.to_dict(orient='records')

def is_valid_for_status(l: list[dict]) -> StatusMessage:
  all_open_item_ids = [r['item_id'] for r in app_tables.bu_item_status.search(is_current=True, status_type='O')]
  all_statuses = [_ for _ in app_tables.bu_statuses.search()]
  all_closed_statuses = [r['status_desc'] for r in all_statuses if r['status_type'] == 'C']

  print(all_open_item_ids)
  for d in l:
    print(d)
    if d['item_id'] not in all_open_item_ids:
      # NEED TO RE-DO THIS.  IF THE ITEM_ID IS LEGIT BUT IT'S ALREADY CLOSED, IT SHOULD JUST BE SKIPPED
      return StatusMessage(False, f"{d['item_id']} is not a currently open item.")
    if d['new_value'] not in all_closed_statuses:
      return StatusMessage(False, f"{d['new_value']} is a not a valid closed status.")

  return StatusMessage(True)

def is_valid_for_ownership(l: list[dict]) -> StatusMessage:
  all_item_owners = [_ for _ in app_tables.bu_item_owner.search()]


  
  candice = df.to_dict(orient='records')
  app_tables.parm.get(what='progress').update(string='d')
  # def questions_datatable_to_list_of_dicts() -> list:
  # this approach takes half as long as returning straight from the search iterator
  csv = app_tables.questions.search().to_csv()
  df = pd.read_csv(BytesIO(csv.get_bytes()))
  # handle the anvil auto-generated ID column
  df.drop(
      columns=['ID', 'created_dt', 'lmt', 'active', 'correct_cnt', 'asked_cnt', 'c_pct', 'difficulty', 'creator'],
      inplace=True)
  # convert the csv peculiarities back to the table data
  df.replace({'final': 0, 'active': 0, 'fave': 0}, False, inplace=True)
  df.replace({'final': 1, 'active': 1, 'fave': 1}, True, inplace=True)
  df.replace({np.nan: None}, inplace=True)
  queso = df.to_dict('records')
  app_tables.parm.get(what='progress').update(string='e')
  # def find_new_and_updated(candice: list, queso: list) -> list:
  queso_qids = [q['id'] for q in queso]
  new = [c for c in candice if c['id'] not in queso_qids]
  for n in new:
      candice.remove(n)
  updated = [c for c in candice if c not in queso]
  expired = [q for q in queso for r in updated if q['id'] == r['id']]
  app_tables.parm.get(what='progress').update(string='f')
  # def insert_new_questions(rows, user_email):
  for r in new:
      app_tables.questions.add_row(**r, **NEW_QUESTION_DEFAULT_VALUES, creator=user_email)
  app_tables.parm.get(what='progress').update(string='g')
  # def insert_q_history(rows, user_email):
  for r in expired:
      app_tables.q_history.add_row(**r, history_date=sm1.LOCAL_NOW, updater=user_email,
                                    version=get_next_version_id_for_question(r['id']))
  app_tables.parm.get(what='progress').update(string='h')
  # def update_questions(rows):
  for r in updated:
      row = app_tables.questions.get(id=r['id'])
      row.update(**r, **UPDATED_QUESTION_DEFAULT_VALUES)
  app_tables.parm.get(what='progress').update(string='i')
  
  # if there were any updates or new questions, write table view and question text to cells on parm table
  if new or updated:
    csv = app_tables.questions.search().to_csv()
    df = pd.read_csv(BytesIO(csv.get_bytes()))
    cols_to_remove = ['tags', 'created_dt', 'lmt', 'creator', 'fave', 'ID']  # ID column is the Anvil-generated row identifier
    df.drop(columns=cols_to_remove, inplace=True)
    # convert the csv peculiarities back to the table data
    df.replace({'final': 0, 'active': 0}, False, inplace=True)
    df.replace({'final': 1, 'active': 1}, True, inplace=True)
    df.replace({np.nan: None}, inplace=True)
    write_this = df.to_dict('records')
    app_tables.parm.get(what='Questions Table').update(obj=write_this, dt=sm1.LOCAL_NOW)
    app_tables.parm.get(what='progress').update(string='j')
    
    q_list = [q['question'].strip() for q in app_tables.questions.search(active=True)]  
    app_tables.parm.get(what='All Questions Text').update(obj=q_list, dt=sm1.LOCAL_NOW)
    app_tables.parm.get(what='progress').update(string='k')
  
  # def write_dt_of_sync():
  row = app_tables.parm.get(what='Last Candice-Queso Sync')
  row.update(dt=sm1.LOCAL_NOW)
  app_tables.parm.get(what='progress').update(string='done')
  return (len(new), len(updated))
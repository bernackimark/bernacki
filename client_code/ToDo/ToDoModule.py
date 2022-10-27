import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

group_color_palate = ['LightBlue', 'LightPink', 'LemonChiffon', 'LightSalmon', 'Gainsboro', 'Aquamarine']
gc_row_list = ['A', 'A', 'A', 'B', 'B', 'B']
gc_col_list = [0, 3, 6, 0, 3, 6]
gc_width = 3

ADD_NEW_GROUP_FROM_NEW_TODO_VALUE = '... add new group ...'

def get_todo_rows(user_email) -> dict:
  to_do_table_view = anvil.server.call('get_user_todos',user_email)
  list_of_todo_dicts = [dict(list(r)) for r in to_do_table_view.search()]
  return list_of_todo_dicts
import anvil.facebook.auth
import anvil.server

group_color_palate = ['LightBlue', 'LightPink', 'LemonChiffon', 'LightSalmon', 'Gainsboro', 'Aquamarine']
gc_row_list = ['A', 'A', 'A', 'B', 'B', 'B']
gc_col_list = [0, 3, 6, 0, 3, 6]
gc_width = 3

ADD_NEW_GROUP_TEXT = '... add new group ...'

def get_todo_rows(user_email) -> dict:
  results = anvil.server.call('get_user_todos',user_email)
  list_of_todo_dicts = [dict(list(r)) for r in results]
  return list_of_todo_dicts
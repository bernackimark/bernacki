import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# dummy data
dummy_data = [{'name': 'Wash Car', 'group': 'House Chores', 'date_added': '2022-10-25'},
              {'name': 'Clean House', 'group': 'House Chores', 'date_added': '2022-10-26'}] 

def get_user_todo_groups(user):
  results = [r['group'] for r in app_tables.todo.search(user=user)]
  my_todo_groups = set()
  for r in results:
    my_todo_groups.add(r)
  return sorted(my_todo_groups)
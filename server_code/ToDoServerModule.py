import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import date, datetime

@anvil.server.callable
def get_user_todos(user_email):
  return app_tables.todos.search(user_email=user_email)

@anvil.server.callable
def get_user_todo_groups(user_email):
  group_as_set = {r['todo_group'] for r in app_tables.todos.search(user_email=user_email, todo_group=q.not_(None))}
  return sorted(list(group_as_set))

@anvil.server.callable
def add_todo(todo_name, todo_group, user_email):
  app_tables.todos.add_row(todo_name=todo_name, todo_group=todo_group, user_email=user_email, date_added=date.today())
  sync_color_w_group(user_email)
  delete_bare_todo_name(todo_group, user_email)
  
@anvil.server.callable
def add_todo_group(todo_group, todo_group_color, user_email):
  app_tables.todos.add_row(todo_group=todo_group, todo_group_color=todo_group_color, user_email=user_email, date_added=date.today())
  
@anvil.server.callable
def update_todo(new_todo_name, new_todo_group, old_todo_name, old_todo_group, user_email):
  row = app_tables.todos.get(todo_name=old_todo_name, todo_group=old_todo_group, user_email=user_email)
  row.update(todo_name=new_todo_name, todo_group=new_todo_group)
  if new_todo_group != old_todo_group:
    new_todo_group_color = sync_color_w_group(user_email)
    return {'todo_name': new_todo_name, 'todo_group': new_todo_group, 'todo_group_color': new_todo_group_color}
  else:
    return {'todo_name': new_todo_name, 'todo_group': new_todo_group, 'todo_group_color': None}

@anvil.server.callable
def delete_todo(item):
  row = app_tables.todos.get(**item)
  row.delete()
  
def sync_color_w_group(user_email):
  existing_user_group_color_pairs = {(r['todo_group'], r['todo_group_color']) for r in app_tables.todos.search(user_email=user_email) if r['todo_group_color'] != None}
  for gcp in existing_user_group_color_pairs:
    for r in app_tables.todos.search(user_email=user_email, todo_group=gcp[0], todo_group_color=None):
      r.update(todo_group_color=gcp[1])
  return gcp[1]
      
def delete_bare_todo_name(todo_group, user_email):
  row = app_tables.todos.get(todo_group=todo_group, user_email=user_email, todo_name=None)
  if row:
    row.delete()
    
  
      
      
  
  
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
  
@anvil.server.callable
def get_user_todos(user_email):
  return app_tables.todos.client_writable(user_email=user_email)

@anvil.server.callable
def add_todo(todo_name, todo_group, user_email):
  app_tables.todos.add_row(todo_name=todo_name, todo_group=todo_group, user_email=user_email)
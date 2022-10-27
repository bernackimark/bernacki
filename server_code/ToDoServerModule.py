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
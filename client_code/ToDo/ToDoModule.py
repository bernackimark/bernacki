import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

group_color_palate = ['LightBlue', 'LightPink', 'LemonChiffon', 'LightSalmon', 'Gainsboro', 'Aquamarine']
ADD_NEW_GROUP_FROM_NEW_TODO_VALUE = '... add new group ...'
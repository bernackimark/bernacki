import anvil.facebook.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# anvil requires dropdown items to be either a list of strings or tuples.  if tuples, it needs ('label', value)
def convert_list_of_ints_to_tuples_for_dd(list_of_int: list) -> list[tuple]:
  return [(str(i), i) for i in list_of_int]

def color_rows(rp: anvil.RepeatingPanel):
  for i, r in enumerate(rp.get_components()):
    if not i%2:
      r.background='theme:Gray 200'

from ._anvil_designer import DiscGolfTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DiscGolf(DiscGolfTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.fl_uploader.file_types = ('xls', 'xlsx')
  
  def fl_uploader_change(self, file, **event_args):
    anvil.server.call('load_spreadsheet', file)


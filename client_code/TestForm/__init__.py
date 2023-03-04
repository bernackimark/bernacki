from ._anvil_designer import TestFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TestForm(TestFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def btn_variable_click(self, **event_args):
    var = anvil.server.call('test_func', self.tb_variable.text)
    self.lbl_variable.text = var

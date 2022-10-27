from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.background = self.item['todo_group_color']
    self.write_drp.visible = False

  def edit_todo_btn_click(self, **event_args):
    self.write_drp.visible, self.read_drp.visible = True, False

  def save_todo_btn_click(self, **event_args):
    todo_name = self.edit_todo_name_tb.text
    todo_group = self.edit_todo_group_dd.selected_value
    
    self.write_drp.visible, self.read_drp.visible = False, True



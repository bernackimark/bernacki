from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import datetime

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.background = self.item['todo_group_color']
    self.write_drp.visible = False

  def edit_todo_btn_click(self, **event_args):
    self.edit_todo_group_dd.items = anvil.server.call('get_user_todo_groups', self.item['user_email'])
    self.write_drp.visible, self.read_drp.visible = True, False
    
  def save_todo_btn_click(self, **event_args):
    new_todo_name = self.edit_todo_name_tb.text
    new_todo_group = self.edit_todo_group_dd.selected_value
    old_todo_name = self.item['todo_name']
    old_todo_group = self.item['todo_group']
    updated_row_dict = anvil.server.call('update_todo', new_todo_name, new_todo_group, old_todo_name, old_todo_group, self.item['user_email'])
    self.todo_name_lbl.text = updated_row_dict['todo_name']
    self.todo_group_lbl.text = updated_row_dict['todo_group']
    if updated_row_dict['todo_group_color'] != None:
      self.background = updated_row_dict['todo_group_color']
    self.write_drp.visible, self.read_drp.visible = False, True



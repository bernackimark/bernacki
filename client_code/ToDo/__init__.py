from ._anvil_designer import ToDoTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from . import ToDoModule as tdm

class ToDo(ToDoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #user_email = anvil.users.get_user()['email']
    # HARDCODE !!!
    user_email = 'bernackimark@gmail.com'
    self.user_email = user_email

    
    self.add_todo_card.visible, self.add_todo_group_card.visible = False, False
    self.add_todo_group_from_todo_tb.visible = False
    
    self.list_of_todo_dicts = self.load_todo_rp()
    
    user_todo_groups = set()
    user_todo_groups.add(tdm.ADD_NEW_GROUP_FROM_NEW_TODO_VALUE)
    list_of_groups = [r['todo_group'] for r in self.list_of_todo_dicts]
    for g in list_of_groups:
      user_todo_groups.add(g)
    self.todo_group_dd.items = sorted(user_todo_groups)
    
    self.color_1_btn.background, self.color_2_btn.background = tdm.group_color_palate[0], tdm.group_color_palate[1]
    self.color_3_btn.background, self.color_4_btn.background = tdm.group_color_palate[2], tdm.group_color_palate[3]
    self.color_5_btn.background, self.color_6_btn.background = tdm.group_color_palate[4], tdm.group_color_palate[5]

  def launch_new_todo_btn_click(self, **event_args):
    self.add_todo_card.visible = True    
    
  def add_todo_cancel_btn_click(self, **event_args):
    self.add_todo_card.visible = False

  def add_todo_btn_click(self, **event_args):
    if self.add_todo_name_tb in ['',None]:
      alert("Please enter a To-do name.")
      return
#     for e in event_args['sender']:
#       print(e)
    todo_name = self.add_todo_name_tb.text
    todo_group = self.todo_group_dd.selected_value
    if self.add_todo_group_from_todo_tb.text != None:
      todo_group = self.add_todo_group_from_todo_tb.text
    anvil.server.call('add_todo', todo_name, todo_group, self.user_email)
    self.add_todo_card.visible = False
    self.load_todo_rp()

  def todo_group_dd_change(self, **event_args):
    if self.todo_group_dd.selected_value == tdm.ADD_NEW_GROUP_FROM_NEW_TODO_VALUE:
      self.add_todo_group_from_todo_tb.visible = True
    else:
      self.add_todo_group_from_todo_tb.visible = False

  def load_todo_rp(self) -> dict:
    to_do_table_view = anvil.server.call('get_user_todos',self.user_email)
    list_of_todo_dicts = [dict(list(r)) for r in to_do_table_view.search()]
    self.todo_rp.items = list_of_todo_dicts
    return list_of_todo_dicts










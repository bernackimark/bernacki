from ._anvil_designer import ToDoTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
from anvil.tables import app_tables

from . import ToDoModule as tdm
from ..user import user

class ToDo(ToDoTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.user_email = user.user['email']
    # user_email = 'bernackimark@gmail.com'  # for testing
    self.selected_group_color = ''

    self.add_todo_card.visible, self.add_todo_group_card.visible = False, False
    self.todo_group_dd.placeholder = ' '
    
    list_of_todo_dicts = tdm.get_todo_rows(self.user_email)
    self.todo_rp.items = list_of_todo_dicts
    
    todo_groups = self.get_todo_groups()
    self.populate_todo_group_dd(todo_groups)
    
    self.populate_group_colors()
    
    if len(list_of_todo_dicts) == 0:
      self.todo_dg.visible = False
    
  def get_todo_groups(self):
    return anvil.server.call('get_user_todo_groups', self.user_email)
  
  def populate_todo_group_dd(self, todo_groups):
    todo_groups = sorted(todo_groups)
    todo_groups.insert(0, ' ')
    todo_groups.insert(1, tdm.ADD_NEW_GROUP_TEXT)
    self.todo_group_dd.selected_value = ' '
    self.todo_group_dd.items = todo_groups
    
  def populate_group_colors(self):
    group_colors = {}
    for idx, color in enumerate(tdm.group_color_palate):
      group_colors[idx] = Button(background=color, text='                                   ')
      group_colors[idx].set_event_handler('click', self.group_color_click)
      group_colors[idx].tag.color = color
    for idx, c in enumerate(group_colors):
      row = int(idx//3)
      col_xs = 4*idx%3
      self.group_color_gp.add_component(group_colors[c], row=row, col_xs=col_xs, width_xs=tdm.gc_width)
    self.set_selected_color()
  
  def group_color_click(self, **event_args):
    sender = event_args['sender']
    color = sender.tag.color
    self.selected_group_color = color
    self.set_selected_color()
  
  def set_selected_color(self):
    for group_color in self.group_color_gp.get_components():
      if group_color.tag.color == self.selected_group_color:
        group_color.border = '2px black solid'
      else:
        group_color.border = ''
  
  def launch_new_todo_btn_click(self, **event_args):
    self.add_todo_card.visible = True  
    
  def add_todo_cancel_btn_click(self, **event_args):
    self.add_todo_card.visible = False

  def add_todo_btn_click(self, **event_args) -> dict:
    if self.add_todo_name_tb in ['', ' ', None]:
      alert("Please enter a To-do name.")
      return
    # get the UI values and add record to the database
    todo_name = self.add_todo_name_tb.text
    todo_group = self.todo_group_dd.selected_value
    success = anvil.server.call('add_todo', todo_name, todo_group, self.user_email)
    if not success:
      alert("You've already added that task.")
      return
    # hide & clear the card
    self.add_todo_card.visible = False
    self.add_todo_name_tb.text = None

    # get the rows again from the db
    list_of_todo_dicts = tdm.get_todo_rows(self.user_email)
    # refresh the repeating panel
    self.refresh_todos()

    todo_groups = self.get_todo_groups()
    self.populate_todo_group_dd(todo_groups)    
    
    # this could have been the user's first row, show the table
    self.todo_dg.visible = True
    return list_of_todo_dicts

  def todo_group_dd_change(self, **event_args):
    if self.todo_group_dd.selected_value == tdm.ADD_NEW_GROUP_TEXT:
      self.add_todo_group_card.visible = True
    else:
      self.add_todo_group_card.visible = False

  def refresh_todos(self):
    self.todo_rp.items = tdm.get_todo_rows(self.user_email)

  def new_todo_group_cancel_btn_click(self, **event_args):
    self.add_todo_group_tb.text = None
    self.add_todo_group_card.visible = False

  def new_todo_group_btn_click(self, **event_args):
    if self.add_todo_group_tb in ['', ' ', None]:
      alert("Please enter a To-do Group name.")
      return
    # get the UI values and add record to the database
    todo_group = self.add_todo_group_tb.text
    anvil.server.call('add_todo_group', todo_group, self.selected_group_color, self.user_email)
    # hide & clear the card
    self.add_todo_group_card.visible = False
    self.add_todo_group_tb.text = None
    # get the rows again from the db
    list_of_todo_dicts = tdm.get_todo_rows(self.user_email)

    todo_groups = self.get_todo_groups()
    self.populate_todo_group_dd(todo_groups)
    
    # set the add todo group dropdown selected_value back to null
    self.todo_group_dd.selected_value = self.todo_group_dd.placeholder
    return list_of_todo_dicts    














from ._anvil_designer import ToDoTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ToDo(ToDoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.header_gp.full_width_row, self.new_todo_gp.full_width_row, self.new_todo_group_gp.full_width_row = True, True, True
    self.todo_dg.full_width_row = True
    self.header_gp.role, self.new_todo_gp.role, self.new_todo_group_gp.role = 'todo-gp', 'todo-gp', 'todo-gp'
    
    self.load_header()
    self.load_new_todo()
    self.load_new_todo_group()
    self.load_to_do_table()
    
  def load_header(self):
    self.header_gp.add_component(Button(text='To-do', icon='fa:calendar-plus-o', icon_align='left', tag='todo_btn'),row=1, col_xs=0, width_xs=2)
    self.header_gp.add_component(Label(align='right', text='My To-do Groups', spacing_above='large', spacing_below='none'), row=1, col_xs=2, width_xs=2)
    self.header_gp.add_component(DropDown(placeholder='...Add Group', items=['a','b']), row=1, col_xs=4, width_xs=3)
    
  def load_new_todo(self):
    self.new_todo_gp.add_component(Label(text='New To-do *'), row=1, col_xs=0, width_xs=3)
    self.new_todo_gp.add_component(TextBox(width=200, tag='new_todo_name'), row=1, col_xs=3, width_xs=2)
    self.new_todo_gp.add_component(Label(text='Assign to To-do Group:'), row=2, col_xs=0, width_xs=3)
    self.new_todo_gp.add_component(DropDown(width=200, tag='new_todo_group_name'), row=2, col_xs=3, width_xs=3)
    self.new_todo_gp.add_component(Button(text='Cancel', tag='new_todo_cancel_btn'), row=2, col_xs=6, width_xs=2)
    self.new_todo_gp.add_component(Button(text='OK', tag='new_todo_ok_btn'), row=2, col_xs=7, width_xs=1)
  
  def load_new_todo_group(self):
    self.new_todo_group_gp.add_component(Label(text='New To-do Group *'))
    self.new_todo_group_gp.add_component(TextBox(width=200, tag='new_todo_group_name'))
    self.new_todo_group_gp.add_component(Button(text='Cancel', tag='new_todo_group_cancel_btn'))
    self.new_todo_group_gp.add_component(Button(text='OK', tag='new_todo_group_ok_btn')) 
    
  def load_to_do_table(self):
    self.todo_dg.columns=['A','B']
    
    
    
    
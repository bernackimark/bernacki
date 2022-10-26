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

    # dummy data
    dummy_data = [{'a': 'Dummy A', 'b': 'Dummy B'}, {'a': 'Dummy A', 'b': 'Dummy B'}]    
    
    self.header_gp.full_width_row, self.new_todo_gp.full_width_row, self.new_todo_group_gp.full_width_row = True, True, True
    self.todo_table_gp.full_width_row = True
    self.header_gp.role, self.new_todo_gp.role, self.new_todo_group_gp.role = 'todo-gp', 'todo-gp', 'todo-gp'
    self.todo_table_gp.role = 'todo-gp'
    
    # Header Components
    todo_btn = Button(text='To-do', icon='fa:calendar-plus-o', icon_align='left', tag='todo_btn')
    todo_groups_lbl = Label(align='right', text='My To-do Groups', spacing_above='large', spacing_below='none')
    todo_dd = DropDown(placeholder='...Add Group', items=['a','b'])
    
    # New To-do Components
    new_todo_lbl = Label(text='New To-do *')
    new_todo_tb = TextBox(width=200)
    new_todo_existing_group_lbl = Label(text='Assign to To-do Group:')
    new_todo_existing_group_dd = DropDown(width=200)
    new_todo_cancel_btn = Button(text='Cancel')
    new_todo_ok_btn = Button(text='OK')
    
    # New To-do Group Components
    new_todo_group_lbl = Label(text='New To-do Group *')
    new_todo_group_tb = TextBox(width=200)
    new_todo_group_cancel_btn = Button(text='Cancel')
    new_todo_group_ok_btn = Button(text='OK')
    
    # To-do Table Components
    todo_table_dg = DataGrid(columns=['a','b'])
    todo_table_rp = RepeatingPanel(items=dummy_data)
    
    # Load all components
    self.load_header(todo_btn, todo_groups_lbl, todo_dd)
    self.load_new_todo(new_todo_lbl, new_todo_tb, new_todo_existing_group_lbl, new_todo_existing_group_dd, new_todo_cancel_btn, new_todo_ok_btn)
    self.load_new_todo_group(new_todo_group_lbl, new_todo_group_tb, new_todo_group_cancel_btn, new_todo_group_ok_btn)
    self.load_to_do_table(todo_table_dg, todo_table_rp)
    
  def load_header(self, todo_btn, todo_group_lbl, todo_dd):
    self.header_gp.add_component(todo_btn, row=1, col_xs=0, width_xs=2)
    self.header_gp.add_component(todo_group_lbl, row=1, col_xs=2, width_xs=2)
    self.header_gp.add_component(todo_dd, row=1, col_xs=4, width_xs=3)
    
  def load_new_todo(self, new_todo_lbl, new_todo_tb, new_todo_existing_group_lbl, new_todo_existing_group_dd, new_todo_cancel_btn, new_todo_ok_btn):
    self.new_todo_gp.add_component(new_todo_lbl, row=1, col_xs=0, width_xs=3)
    self.new_todo_gp.add_component(new_todo_tb, row=1, col_xs=3, width_xs=2)
    self.new_todo_gp.add_component(new_todo_existing_group_lbl, row=2, col_xs=0, width_xs=3)
    self.new_todo_gp.add_component(new_todo_existing_group_dd, row=2, col_xs=3, width_xs=3)
    self.new_todo_gp.add_component(new_todo_cancel_btn, row=2, col_xs=6, width_xs=2)
    self.new_todo_gp.add_component(new_todo_ok_btn, row=2, col_xs=8, width_xs=1)
  
  def load_new_todo_group(self, new_todo_group_lbl, new_todo_group_tb, new_todo_group_cancel_btn, new_todo_group_ok_btn):
    self.new_todo_group_gp.add_component(new_todo_group_lbl, row=1, col_xs=0, width_xs=3)
    self.new_todo_group_gp.add_component(new_todo_group_tb, row=1, col_xs=3, width_xs=2)
    self.new_todo_group_gp.add_component(new_todo_group_cancel_btn, row=2, col_xs=0, width_xs=2)
    self.new_todo_group_gp.add_component(new_todo_group_ok_btn, row=2, col_xs=2, width_xs=1) 
    
  def load_to_do_table(self, todo_table_dg, todo_table_rp):
    self.todo_table_gp.add_component(todo_table_dg)
    todo_table_dg.add_component(todo_table_rp)
    
    
    
    
from ._anvil_designer import ToDoTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import ToDoModule as tdm

class ToDo(ToDoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #user_email = anvil.users.get_user()['email']
    # HARDCODE !!!
    user_email = 'bernackimark@gmail.com'
    

    
    self.add_todo_card.visible, self.add_todo_group_card.visible = False, False
    
    to_do_table_view = anvil.server.call('get_user_todos',user_email)
    self.todo_rp.items = [r for r in to_do_table_view.search()]
    
    self.color_1_btn.background, self.color_2_btn.background = tdm.group_color_palate[0], tdm.group_color_palate[1]
    self.color_3_btn.background, self.color_4_btn.background = tdm.group_color_palate[2], tdm.group_color_palate[3]
    self.color_5_btn.background, self.color_6_btn.background = tdm.group_color_palate[4], tdm.group_color_palate[5]
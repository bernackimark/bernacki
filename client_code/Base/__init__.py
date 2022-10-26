from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home
from ..Setback import Setback
from ..Setback.SetbackBotChallenge import SetbackBotChallenge
from ..ToDo import ToDo

class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.my_stuff.width, self.sign_in.width = 130, 115
    self.links_sidebar_cp.width = 100
    self.show_my_stuff_link()
    self.change_sign_in_text()
    # self.content_panel.add_component(Home())
    
    user = anvil.users.get_user()
  
  def go_to_base(self):
    self.content_panel.clear()
    self.content_panel.add_component(Base())

  def go_home_link_click(self, **event_args):
    self.go_to_base()    
    
  def my_stuff_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Home())

  def show_my_stuff_link(self):
    self.my_stuff.visible = anvil.users.get_user() != None

  def todo_link_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(ToDo())    
    
  def sign_in_click(self, **event_args):
    user = anvil.users.get_user()
    if user:
      logout = confirm("Logout?")
      if logout:
        anvil.users.logout()
        self.go_to_base()
    else:
      anvil.users.login_with_form()
    self.change_sign_in_text()
    self.show_my_stuff_link()

  def change_sign_in_text(self):
    user = anvil.users.get_user()
    if user:
      self.sign_in.text = user['email']
      self.sign_in.width = len(user['email']) * 20
    else:
      self.sign_in.text = "Sign In"
  








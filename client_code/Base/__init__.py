from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..Admin import Admin
from ..Bets.ProposeBet import ProposeBet
from ..Bets.SelfBet import SelfBet
from ..DiscGolf import DiscGolf
from ..FeaturesFeedback import FeaturesFeedback
from ..Games import Games
from ..Games.Cribbage import Cribbage
from ..Games.Mastermind import Mastermind
from ..Games.Setback import Setback
from ..Games.Setback.SetbackBotChallenge import SetbackBotChallenge
from ..ToDo import ToDo
from ..TripBuilder import TripBuilder

class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.go_home_link.icon = '_/theme/bernacki_logo.png'
    self.change_sign_in_text()
    # self.content_panel.add_component(Home())
    
    user = anvil.users.get_user()
  
  def go_to_base(self):
    self.content_panel.clear()

  def go_home_link_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.go_to_base()  
    
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

  def change_sign_in_text(self):
    user = anvil.users.get_user()
    if user:
      self.sign_in.text = user['email']
      self.sign_in.width = len(user['email']) * 20
    else:
      self.sign_in.text = "Sign In"

  def link_dg_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(DiscGolf())

  def link_admin_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(Admin())

  def link_trip_builder_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(TripBuilder())

  def cp_link_highlights(self, **e):
    for l in self.cp_links.get_components():
      if type(l) is Link:
        l.role = ''
    e['sender'].role = 'selected'

  def link_bets_click(self, **event_args):
    for o in self.link_bets.get_components():
      if type(o) is Link:
        if o.visible == False:
          o.visible = True
        else:
          o.visible = False

  def link_bets_propose_bet_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(ProposeBet())

  def link_self_bet_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(SelfBet())

  def link_feedback_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(FeaturesFeedback())

  def link_mastermind_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(Mastermind())

  def link_setback_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(Setback())

  def link_games_click(self, **event_args):
    for o in self.link_games.get_components():
      if type(o) is Link:
        if o.visible == False:
          o.visible = True
        else:
          o.visible = False

  def link_todo_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    self.content_panel.add_component(ToDo())

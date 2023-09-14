from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .IntentionalBlankForm import IntentionalBlankForm
from .PostCard import PostCard

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
from ..Games.Slots import Slots
from ..SoundVisualizer import SoundVisualizer
from ..ToDo import ToDo
from ..TripBuilder import TripBuilder

from ..user import user

app_form_dict = {'admin': Admin, 'propose_bet': ProposeBet, 'self_bet': SelfBet, 'disc_golf': DiscGolf,
                 'feedback': FeaturesFeedback,
                 'cribbage': Cribbage, 'mastermind': Mastermind, 'setback': Setback, 'slots': Slots,
                 'sound_visualizer': SoundVisualizer, 'todo': ToDo, 'trip_builder': TripBuilder}


from datetime import datetime

class Base(BaseTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.go_home_link.icon = '_/theme/bernacki_logo.png' 
    self.show_app_links()
    self.show_posts()

  def go_home_link_click(self, **event_args):
    self.cp_link_highlights(**event_args)
    self.content_panel.clear()
    
  def sign_in_click(self, **event_args):
    if user.logged_in:
      logout = confirm("Logout?")
      if logout:
        user.logout()
        anvil.users.logout()
        self.change_sign_in_text()
        self.content_panel.clear()
        self.show_app_links()
      return
    anvil.users.login_with_form()
    user.login()
    self.show_app_links()
    self.change_sign_in_text()

  def show_app_links(self):
    self.cp_links.clear()
    my_apps = anvil.server.call('get_my_apps_as_dicts', user.user)
    my_app_groups = sorted({a['group'] for a in my_apps})
    for ag in my_app_groups:
      link_group = Link(text=ag if ag else 'Uncategorized', align='center', font_size=18)
      link_group.add_event_handler('click', lambda **e: self.link_group_click(**e))
      self.cp_links.add_component(link_group)
      for a in my_apps:
        if a['group'] == ag:
          a['icon_str'] = None if a['icon_str'] == '' else a['icon_str']
          link = Link(text=a['title'], align='center', font_size=18, icon_align='top', icon=a['icon_str'])
          link.tag = a['name']
          link.add_event_handler('click', self.app_link_click)
          link.visible = False
          link_group.add_component(link)
  
  def app_link_click(self, **e):
    app_name = e['sender'].tag
    self.cp_link_highlights(**e)
    self.content_panel.clear()
    if app_name not in app_form_dict.keys():
      self.content_panel.add_component(IntentionalBlankForm())
      return
    self.content_panel.add_component(app_form_dict[app_name]())

  def change_sign_in_text(self):
    if user.logged_in:
      self.sign_in.text = user.user['email']
      self.sign_in.width = len(user.user['email']) * 10
    else:
      self.sign_in.text = "Sign In"

  def cp_link_highlights(self, **e):
    for l in self.cp_links.get_components():
      if type(l) is Link:
        l.role = ''
    e['sender'].role = 'selected'

  def link_group_click(self, **e):
    for o in e['sender'].get_components():
      if type(o) is Link:
        o.visible = False if o.visible else True

  def show_posts(self):
    self.rp_posts.items = [{'avatar': '_/theme/cat_cropped.png', 'handle': 'Bernacki', 'time_ago': '1h ago', 
                            'body': ['Lorem ipsum dolor ' * 10], 'like_cnt': 5, 'comment_cnt': 7, 'has_user_liked': True,
                            'title': 'Post #3', 'comments': [{'avatar': '_/theme/maroon_tile.png', 'handle': 'Micky Maroon', 'text': 'My son says your website stinks!', 'time_ago': '1s ago'}]},
                          {'avatar': '_/theme/cat_cropped.png', 'handle': 'Bernacki', 'time_ago': 'Two weeks ago', 
                            'body': ['Lorem ipsum dolor ' * 25], 'like_cnt': 0, 'comment_cnt': 0, 'has_user_liked': False,
                            'title': 'Post #2: The One About the Thing', 'comments': [{'avatar': '_/theme/gold_tile.png', 'handle': 'Glenda Golden', 'text': '0 out of 5 stars. Would not recommend ...', 'time_ago': '2h ago'}]},
                          {'avatar': '_/theme/cat_cropped.png', 'handle': 'Bernacki', 'time_ago': 'Two months ago', 
                            'body': ['Lorem ipsum dolor ' * 25], 'like_cnt': 0, 'comment_cnt': 0, 'has_user_liked': False,
                            'title': 'Announcing the Bernacki Website!!!', 'comments': []}]

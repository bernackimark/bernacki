from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.facebook.auth
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ...user import user

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    if dict(self.item).get('app'):
      self.lbl_app_title.text = [a['title'] for a in user.my_apps if self.item['app'] == a['name']][0]

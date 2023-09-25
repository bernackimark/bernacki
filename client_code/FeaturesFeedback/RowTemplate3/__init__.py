from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.facebook.auth
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import client_side_general_module as m

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    if dict(self.item).get('app'):
      self.lbl_app_title.text = m.my_apps.get_app_title_from_name(self.item['app'])

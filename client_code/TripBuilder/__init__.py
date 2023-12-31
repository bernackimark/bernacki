from ._anvil_designer import TripBuilderTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
from anvil.tables import app_tables

from . import trip_builder_module as m
from ..user import user

class TripBuilder(TripBuilderTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.display_trip_builder()
    self.rp_build_trip.set_event_handler('x-refresh-trip-builder', self.display_trip_builder)

    if not user.logged_in:
      self.dd_known_collections.items = anvil.server.call('get_user_known_collections', None)
    else:
      self.dd_known_collections.items = anvil.server.call('get_user_known_collections', user.user['email'])
  
  def btn_build_trip_click(self, **event_args):
    for row in self.rp_build_trip.items:
      if row['name'] in ('', None):
        alert('Please enter a location into each row')
        return
    if sum([r['orig'] for r in self.rp_build_trip.items]) != 1 or sum([r['dest'] for r in self.rp_build_trip.items]) != 1:
      alert('Please check exactly one box for origin and destination')
      return
    if [idx for idx, r in enumerate(self.rp_build_trip.items) if r['orig']][0] == [idx for idx, r in enumerate(self.rp_build_trip.items) if r['dest']][0]:
      alert('Please have a different origin & destination.  It is currently a Beta limitation.')
      return
    self.expand_collapse_trip_builder_card('collapse')
    res = anvil.server.call('run_geo', self.rp_build_trip.items)
    self.display_my_routes(res)
    m.update_lat_long_from_db(res)
    self.display_trip_builder()
    
  def display_my_routes(self, data: list[dict]):
    self.rp_my_routes.items = sorted(data, key=lambda x: x['duration'])

  def display_trip_builder(self, **e):
    self.rp_build_trip.items = m.trip_builder_items
    if len(m.trip_builder_items) < 7:
      self.btn_add_point.enabled = True

  def btn_add_point_click(self, **event_args):
    if len(m.trip_builder_items) >= 7:
      alert('Our Beta currently only allows for seven points max')
      return
    m.add_item()
    self.display_trip_builder()
    if len(m.trip_builder_items) >= 7:
      self.btn_add_point.enabled = False

  def btn_expand_collapse_trip_builder_card_click(self, **event_args):
    if self.btn_expand_collapse_trip_builder_card.icon == 'fa:chevron-up':
      self.expand_collapse_trip_builder_card('expand')
    else:
      self.expand_collapse_trip_builder_card('collapse')

  def expand_collapse_trip_builder_card(self, action: str):
    if action == 'collapse':
      self.btn_expand_collapse_trip_builder_card.icon = 'fa:chevron-up'
      self.lbl_instructions.visible = self.cp_collections.visible = self.dg_build_trip.visible = self.btn_build_trip.visible = False
    elif action == 'expand':
      self.btn_expand_collapse_trip_builder_card.icon = 'fa:chevron-down'
      self.lbl_instructions.visible = self.cp_collections.visible = self.dg_build_trip.visible = self.btn_build_trip.visible = True
    else:
      pass

  def dd_known_collections_change(self, **event_args):
    m.trip_builder_items = anvil.server.call('get_known_points', self.dd_known_collections.selected_value)
    self.display_trip_builder()

  def btn_save_collection_click(self, **event_args):
    if not user.logged_in:
      alert("You must be signed in to save a collection.  It's free to do so.")
      return
    if not user.user['confirmed_email']:
      alert("Please perform the e-mail verification step in order to complete the sign-up process.")
      return
    for p in m.trip_builder_items:
      if p['name'] in ['', None] or p['lat_long'] in [(), None]:
        alert('To create a collection, first create a list of points & coordinates.  To obtain coordinates, enter a good description for your points, then click on the Build My Trip button.')
        return
    if len(m.trip_builder_items) < 3:
      alert('You must have at least three points to save a collection.')
      return
    tb_new_coll = TextBox(placeholder='Enter the name for your collection here')
    c = confirm(content=tb_new_coll, large=True, title='Save Your Collection?')
    if c:
      anvil.server.call('create_known_collection_and_points', coll_name=tb_new_coll.text, email=user.user['email'], points=m.trip_builder_items)
    

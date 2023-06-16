from ._anvil_designer import DiscGolfTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import dg_module as dgm
from .. import utils

class DiscGolf(DiscGolfTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = dgm.sort_dg_events('end_date', True)
    # self.repeating_panel_1.items = app_tables.dg_events.search(tables.order_by("end_date", ascending=False))
    self.dd_mpo_champions.items = dgm.filter_sort_unique_column('mpo_champion')
    self.dd_fpo_champions.items = dgm.filter_sort_unique_column('fpo_champion')
    self.dd_events.items = dgm.filter_sort_unique_column('name')
    self.dd_state.items = dgm.filter_sort_unique_column('state')
    self.dd_country.items = dgm.filter_sort_unique_column('country')
    self.dd_governing_body.items = dgm.filter_sort_unique_column('governing_body')
    self.dd_designation.items = dgm.filter_sort_unique_column('designation')
    self.dd_time_period.items = utils.time_periods

    for o in self.card_filter.get_components():
      if type(o) is DropDown:
        o.tag = 'filter_dd'  # this allows me to identify all dropdown components in the card_filter
        o.include_placeholder = True  # so i don't forget to include a placeholder for each dropdown
    
    # self.fl_uploader.file_types = ('xls', 'xlsx')
  
  def fl_uploader_change(self, file, **event_args):
    anvil.server.call('load_spreadsheet', file)

  def dd_mpo_champions_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_mpo_champions)
    self.repeating_panel_1.items = dgm.filter_sort_by_date_desc('mpo_champion', self.dd_mpo_champions.selected_value)

  def dd_fpo_champions_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_fpo_champions)
    self.repeating_panel_1.items = dgm.filter_sort_by_date_desc('fpo_champion', self.dd_fpo_champions.selected_value)

  def dd_events_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_events)
    self.repeating_panel_1.items = dgm.filter_sort_by_date_desc('name', self.dd_events.selected_value)
  
  def dd_state_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_state)
    self.repeating_panel_1.items = dgm.filter_sort_by_date_desc('state', self.dd_state.selected_value)

  def dd_country_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_country)
    self.repeating_panel_1.items = dgm.filter_sort_by_date_desc('country', self.dd_country.selected_value)

  def dd_governing_body_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_governing_body)
    self.repeating_panel_1.items = dgm.filter_sort_by_date_desc('governing_body', self.dd_governing_body.selected_value)

  def dd_designation_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_designation)
    self.repeating_panel_1.items = dgm.filter_sort_by_date_desc('designation', self.dd_designation.selected_value)

  def dd_time_period_change(self, **event_args):
    self.clear_all_other_dd_selections(self.dd_time_period)
    self.repeating_panel_1.items = dgm.filter_by_time_period(self.dd_time_period.selected_value)

  def clear_all_other_dd_selections(self, the_current_dd):
    for o in self.card_filter.get_components():
      if o.tag == 'filter_dd' and o != the_current_dd:
          o.selected_value = None

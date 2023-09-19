from ._anvil_designer import AdminDGTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ...DiscGolf import dg_module as dgm
from ... import user
from ... import utils_for_anvil as ua

class AdminDG(AdminDGTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        dgm.dg_data = dgm.get_dg_data()
        dgm.dg_event_names = [{'id': r['id'], 'name': r['name'], 'city': r['city'], 'state': r['state'], 'country': r['country']} for r in app_tables.dg_tournaments.search()]
        self.dd_event_name.items = [(f"{r['name']} ({r['city']}, {r['state']}, {r['country']})", r['id']) for r in dgm.dg_event_names]
        self.dd_governing_body.items = dgm.filter_sort_unique_column('governing_body')
        self.dd_designation.items = dgm.filter_sort_unique_column('designation')
        self.dd_mpo_champ.items = dgm.filter_sort_unique_column('mpo_champion')
        self.dd_fpo_champ.items = dgm.filter_sort_unique_column('fpo_champion')
        self.get_most_recent_loaded_event()

    def get_most_recent_loaded_event(self):
        max_created_ts = max(r['created_ts'] for r in dgm.dg_data)
        last_created_event_name, last_created_event_ts = [(r['name'], r['created_ts']) for r in dgm.dg_data if r['created_ts'] == max_created_ts][0]
        self.lbl_last_event_added.text = f'Last Event Added:{chr(10)}{last_created_event_name} ({last_created_event_ts:%m.%d.%Y %H:%M:%S})' 
    
    def btn_add_new_dg_event_click(self, **event_args):
        mpo_champ_row = app_tables.dg_players.get(full_name=self.dd_mpo_champ.selected_value)
        fpo_champ_row = app_tables.dg_players.get(full_name=self.dd_fpo_champ.selected_value)
        tourney_row = app_tables.dg_tournaments.get(id=self.dd_event_name.selected_value)
        anvil.server.call('write_dg_event', governing_body=self.dd_governing_body.selected_value,
                        designation=self.dd_designation.selected_value, start_date=self.dp_start.date, end_date=self.dp_end.date,
                        mpo_champ_link=mpo_champ_row, fpo_champ_link=fpo_champ_row, tourney_link=tourney_row)
        self.get_most_recent_loaded_event()
    
    def btn_clear_click(self, **e):
        self.clear_all_components_in_parent(**e)
    
    def btn_save_new_golfer_click(self, **event_args):
        for o in self.card_add_new_golfer.get_components():
            if (type(o) is TextBox and not o.text) or (type(o) is DatePicker and not o.date) or (type(o) is DropDown and not o.selected_value):
                alert('You missed some data')
                return
        app_tables.dg_players.add_row(pdga_id=self.tb_pdga_id.text, first_name=self.tb_first_name.text,
                            last_name=self.tb_last_name.text, division=self.dd_division.selected_value)

    def btn_clear_new_golfer_click(self, **e):
        self.clear_all_components_in_parent(**e)

    def btn_save_new_tourney_name_click(self, **event_args):
        app_tables.dg_tournaments.add_row(city=self.tb_new_tourney_city.text, state=self.tb_new_tourney_state.text,
                                          country=self.tb_new_tourney_country.text, name=self.tb_new_tourney_name.text,
                                          id=max([r['id'] for r in app_tables.dg_tournaments.search()])+1)

    def clear_all_components_in_parent(self, **e):  # expects an anvil event
        for o in e['sender'].parent.get_components():
            if type(o) is TextBox:
                o.text = None
            elif type(o) is DatePicker:
                o.date = None
            elif type(o) is DropDown:
                o.selected_value = None
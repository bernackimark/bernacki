from ._anvil_designer import AdminAppsTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AdminApps(AdminAppsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def btn_update_app_click(self, **event_args):
        anvil.server.call('update_app', self.tb_app_name.text, self.tb_key.text, self.tb_value.text)
    
    def btn_add_new_app_click(self, **event_args):
        if not self.tb_new_app_name.text or not self.tb_new_app_title.text:
            alert('Enter a name and title, dumbass')
            return
        
        anvil.server.call_s('write_new_app', name=self.tb_new_app_name.text, title=self.tb_new_app_title.text,
                            group=self.tb_new_app_group.text,
                            user=user.user, icon_str=self.tb_icon_str.text, security=self.dd_security.selected_value)

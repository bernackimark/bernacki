from ._anvil_designer import CompleteRegistrationTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CompleteRegistration(CompleteRegistrationTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.btn_save_completed_registration.enabled = False

    def tb_complete_reg_handle_change(self, **event_args):
        if len(self.tb_complete_reg_handle.text) >= 3:
            self.btn_save_completed_registration.enabled = True
        else:
            self.btn_save_completed_registration.enabled = False

    def btn_save_completed_registration_click(self, **event_args):
        self.raise_event("x-close-alert", value=[self.tb_complete_reg_handle.text, self.fl_complete_reg_avatar.file])
        # it seems the when using the built-in x-close-alert, the return value's
        # variable name must be "value"
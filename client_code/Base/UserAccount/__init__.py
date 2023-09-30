from ._anvil_designer import UserAccountTemplate
from anvil import *
import anvil.server

from ...user import user

class UserAccount(UserAccountTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def file_loader_1_change(self, file, **event_args):
        user.update_avatar(file)

    def btn_logout_click(self, **event_args):
        user.logout()
        self.raise_event("x-close-alert")


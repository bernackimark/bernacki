import anvil.server
import anvil.users

# important to have this in a module because having anvil.users.get_user() is an expensive server call
# don't forget to use user.user (not just user) to get the user row dictionary
class User:
    def __init__(self):
        self.user: dict = None
        self.logged_in: bool = False
        self.my_apps: list[dict] = anvil.server.call('get_my_apps_as_dicts', None)

    @property
    def my_app_groups(self) -> list[str]:
        return sorted({a['group'] for a in self.my_apps})

    def login(self):
        self.user = anvil.users.get_user()
        self.logged_in = True
        self.my_apps: list[dict] = anvil.server.call('get_my_apps_as_dicts', self.user)

    def logout(self):
        self.user = None
        self.logged_in = False
        self.my_apps: list[dict] = anvil.server.call('get_my_apps_as_dicts', None)

    def update_handle_and_avatar(self, handle, avatar):
        anvil.server.call('update_handle_and_avatar', handle, avatar)
        self.user = anvil.users.get_user()


user = User()

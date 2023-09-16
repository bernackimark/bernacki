import anvil.server
import anvil.users


# important to have this in a module because having anvil.users.get_user() is a server call
# having in the forms is expensive
# don't forget to use user.user to get the user row dictionary
class User:
    def __init__(self):
        self.user: dict = None
        self.logged_in: bool = False

    def login(self):
        self.user = anvil.users.get_user()
        self.logged_in = True

    def logout(self):
        self.user = None
        self.logged_in = False


user = User()
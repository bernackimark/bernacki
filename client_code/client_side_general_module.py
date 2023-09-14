import anvil.server

from .user import user

class MyApps:
  def __init__(self):
    self.my_apps_as_dict = anvil.server.call('get_my_apps_as_dicts', user)

  @property
  def name_and_title_tuples(self):
    return [(a['title'], a['name']) for a in self.my_apps_as_dict]

  def get_app_title_from_name(self, app_name) -> str:
    return [a['title'] for a in self.my_apps_as_dict if app_name == a['name']][0]

my_apps: MyApps

# my_apps_as_dict: list[dict]

# def get_my_apps_as_dict():
#   my_apps_as_dict = anvil.server.call('get_my_apps_as_dicts', user)




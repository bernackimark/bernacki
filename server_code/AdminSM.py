import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from dataclasses import dataclass, field, asdict
import uuid
from datetime import datetime
from enum import Enum


class SecurityLevels(Enum):
    ADMIN = 'admin'
    PRIVATE = 'private'
    PUBLIC = 'public'
    TESTING = 'testing'


@dataclass
class App:
    name: str
    title: str
    created_by: str
    icon_str: str = ''
    security: str = SecurityLevels.TESTING.value
    id: str = str(uuid.uuid4())
    created_ts: datetime = datetime.now().isoformat()
    history: list = field(default_factory=list)


# require_user can take a boolean or a function.  if given a function, that function will receive the currently logged in user (the return value of anvil.users.get_user())
@anvil.server.callable(require_user = lambda u: u['is_admin'])
def get_all_apps() -> list[tuple]:
  r = app_tables.parms.get(what='app_list')
  return [(v['title'], v['name']) for v in r['value']]

@anvil.server.callable
def get_my_apps(user) -> list[tuple]:
  r = app_tables.parms.get(what='app_list')
  if not user:
      return [(a['title'], a['name']) for a in r['value'] if a['security'] == 'public']
  if user['is_admin']:
      return [(a['title'], a['name']) for a in r['value']]
  if user['is_tester']:
      return [(a['title'], a['name']) for a in r['value'] if a['security'] != 'admin']
  if user:
      return [(a['title'], a['name']) for a in r['value'] if a['security'] in ['public', 'private']]

@anvil.server.callable(require_user = lambda u: u['is_admin'])
def write_new_app(name: str, title: str, user, icon_str: str, security: str):
  app = App(name=name, title=title, created_by=user['email'], icon_str=icon_str, security=security)
  d = asdict(app)
  r = app_tables.parms.get(what='app_list')
  if not r['value']:
    r['value'] = []
  values = r['value']
  values.append(d)
  r['value'] = values


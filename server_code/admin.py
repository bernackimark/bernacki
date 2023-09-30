import anvil.facebook.auth
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
    group: str
    icon_str: str
    created_by: str
    default_info: dict = field(default_factory=dict)
    is_prod: bool = False
    security: str = SecurityLevels.ADMIN.value
    id: str = str(uuid.uuid4())
    created_ts: str = datetime.utcnow().isoformat()
    history: list = field(default_factory=list)

    @property
    def history_record(self):
        return {'name': self.name, 'title': self.title, 'group': self.group, 'icon_str': self.icon_str,
                'default_info': self.default_info,
                'is_prod': self.is_prod, 'security': self.security, 'history_date': datetime.utcnow().isoformat}


@dataclass
class Apps:
    apps: list[App] = field(default_factory=list)

    def __post_init__(self):
        self.apps = [App(**a) for a in app_tables.parms.get(what='app_list')['value']]

    def sort_apps(self, *attribute_names):
        def key_function(items):
            # Sort by the attributes, but place None values at the end
            key_values = []
            for attribute_name in attribute_names:
                value = getattr(items, attribute_name)
                key_values.append((value is None, value))
            return key_values

        self.apps.sort(key=key_function)


def get_all_apps() -> list[App]:
    apps = Apps()
    apps.sort_apps('group', 'name')
    return apps.apps


@anvil.server.callable
def get_my_apps(user=None):
    app_list = get_all_apps()
    if not user:
        return [a for a in app_list if a.is_prod and a.security == SecurityLevels.PUBLIC.value]
    if user:
        # user_row = app_tables.users.get(email=user['email'])
        if user['is_admin']:
            return app_list
        return [a for a in app_list if a.is_prod and a.security in [SecurityLevels.PUBLIC.value, SecurityLevels.PRIVATE.value]]


@anvil.server.callable(require_user=lambda u: u['is_admin'])
def update_app(app_name, key, value):
    row = app_tables.parms.get(what='app_list')
    list_of_dicts = [_ for _ in row['value']]
    app = [app for app in list_of_dicts if app['name'] == app_name][0]
    app_snapshot = App(**app).history_record
    app[key] = value
    app['history'].append(app_snapshot)
    row['value'] = list_of_dicts
    print(f'Updated app: {app_name}')


@anvil.server.callable
def get_my_apps_as_dicts(user=None):
    app_list = get_all_apps()
    if not user:
        return [a.__dict__ for a in app_list if a.is_prod and a.security == SecurityLevels.PUBLIC.value]
    if user:
        if user['is_admin']:
            return [a.__dict__ for a in app_list]
        return [a.__dict__ for a in app_list if a.security in [SecurityLevels.PUBLIC.value, SecurityLevels.PRIVATE.value]]
  

@anvil.server.callable(require_user=lambda u: u['is_admin'])
def write_new_app(name: str, title: str, group: str, user, icon_str: str, security: str):
    if name in [a.name for a in get_all_apps(user)]:
        print('That app name already exists')
        return
    app = App(name=name, title=title, group=group, icon_str=icon_str, created_by=user['email'], security=security)
    row = app_tables.parms.get(what='app_list')
    if not row['value']:
        row['value'] = []
    values = row['value']
    values.append(app.__dict__)
    row['value'] = values


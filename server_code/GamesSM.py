import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GamesLog:
    game_name: str
    game_start_ts: datetime
    game_end_ts: datetime
    player_emails: list[str] = field(default_factory=list)
    game_data: dict = field(default_factory=dict)
    id: int = len(app_tables.games_log.search()) + 1

    def as_dict(self):
        return self.__dict__


@anvil.server.callable
def write_game_data(d: dict, updated_player_data: dict = {}):
    game_class = GamesLog(**d)
    record = game_class.as_dict()
    app_tables.games_log.add_row(**record)

    if updated_player_data:
        update_player_data(game_class.player_emails[0], updated_player_data)


def update_player_data(user_email: str, d: dict):
    user_row = app_tables.users.get(email=user_email)
    user_row_info: dict = user_row['info']
    for k, v in d.items():
        if k in user_row_info.keys():
            user_row_info[k] = v
    user_row['info'] = user_row_info

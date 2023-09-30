import anvil.facebook.auth
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
    player_email: str
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
        update_player_data(game_class.player_email, updated_player_data)


@anvil.server.callable
def update_player_info(user_email: str, d: dict):
    user_row = app_tables.users.get(email=user_email)
    user_row_info: dict = user_row['info']
    if user_row_info:
        for k, v in d.items():
            if k in user_row_info.keys():
                user_row_info[k] = v
        user_row['info'] = user_row_info
    else:  # user_row['info'] is blank
        user_row['info'] = d

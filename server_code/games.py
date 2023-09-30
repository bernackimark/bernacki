import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users

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
        update_player_data(updated_player_data)


@anvil.server.callable
def write_game_data_and_player_info(*, game_data: dict = {}, updated_player_data: dict = {}):
    if game_data:
        game_class = GamesLog(**game_data)
        record = game_class.as_dict()
        app_tables.games_log.add_row(**record)

    if updated_player_data:
        update_player_info(d['game_name'], updated_player_data)


@anvil.server.callable
def update_player_info(app_name: str, d: dict):  # does accepting a user here avoid another look-up?
    user_row = anvil.users.get_user()
    
    # brand new user
    if not user_row['info']:
        user_row['info'] = d
        print(user_row['info'])
        return
        
    game_dict = [d.get(app_name) for d in user_row['info'] if d.get(app_name)]
    # user hasn't played game before
    if not game_dict:
        user_row['info'].append({app_name: d})
        print(user_row['info'])
        return

    # user has played game before
    game_dict = game_dict[0]
    for k, v in d.items():
        game_dict[k] = v


# @anvil.server.callable
# def update_player_info(user_email: str, d: dict):
#     user_row = app_tables.users.get(email=user_email)
#     user_row_info: dict = user_row['info']
#     if user_row_info:
#         for k, v in d.items():
#             if k in user_row_info.keys():
#                 user_row_info[k] = v
#         user_row['info'] = user_row_info
#     else:  # user_row['info'] is blank
#         user_row['info'] = d

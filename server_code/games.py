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
def write_game_data(d: dict):
    game_class = GamesLog(**d)
    record = game_class.as_dict()
    app_tables.games_log.add_row(**record)

    if d['game_name'] == 'slots':
        update_player_info('slots', {'balance': d['game_data']['ending_bal']})


def update_player_info(app_name: str, d: dict):  # does accepting a user here avoid another look-up?
    user_row = anvil.users.get_user()
    
    print(app_name, d)
    
    # brand new user
    if not user_row['info']:
        user_row['info'] = {app_name: d}
        return
        
    game_dict = [d.get(app_name) for d in user_row['info'] if d.get(app_name)]
    # user hasn't played game before
    if not game_dict:
        new_info = user_row['info']
        new_info.append({app_name: d})
        user_row['info'] = new_info
        return

    # user has played game before
    game_dict = game_dict[0]
    for k, v in d.items():
        game_dict[k] = v

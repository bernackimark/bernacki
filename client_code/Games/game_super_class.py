import anvil.server
from datetime import datetime
from ..user import user

class Game:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, game_name: str):
        self.game_name = game_name
        self.game_start_ts = datetime.utcnow()
        self.game_end_ts = None
        self.player_email = user.user['email']
        self.player_info = user.user['info']
        self.game_data = {}  # this is an empty dict which will get populated by the child game
        
    @property
    def as_dictionary(self) -> dict:
        return self.__dict__

    @property
    def parent_class_dict(self) -> dict:
        return {'game_name': self.game_name, 'game_start_ts': self.game_start_ts, 'game_end_ts': self.game_end_ts,
                'player_email': self.player_email, 'game_data': self.game_data}

    def write_game_to_db(self):
        self.game_end_ts = datetime.utcnow()
        anvil.server.call('write_game_data', self.parent_class_dict)

    def update_player_info(self, d: dict):
        anvil.server.call('update_player_info', self.player_email, d)

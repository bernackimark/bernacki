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
        self.user_info = user.user.get('info')
        self.player_game_info = self.get_player_game_info()
        self.game_data = {}  # this is an empty dict which will get populated by the child game

    @property
    # this could be useful to see if we want to display some intstructions
    def has_played_this_game(self) -> bool:
        if self.user_info and [1 for game_dict in self.user_info if self.game_name in game_dict.keys()]:
            return True
        return False

    def get_player_game_info(self):
        if not self.has_played_this_game:

            # the app should have a default dict !!!!
            return ['slots', {'balance': 100}]
            
        return [g for g in self.user_info if g[0] == self.game_name][0]
        
    
    @property
    def parent_class_dict(self) -> dict:
        return {'game_name': self.game_name, 'game_start_ts': self.game_start_ts, 'game_end_ts': self.game_end_ts,
                'player_email': self.player_email, 'game_data': self.game_data}

    def write_game_to_db(self):
        self.game_end_ts = datetime.utcnow()
        anvil.server.call('write_game_data', self.parent_class_dict)

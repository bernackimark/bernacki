import anvil.server
from datetime import datetime


class Game:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, game_name: str, player_emails: list[str] = [], game_data: dict = dict()):
        self.game_name = game_name
        self.game_start_ts = datetime.utcnow()
        self.game_end_ts = None
        self.player_emails = player_emails
        self.game_data = game_data

    @property
    def as_dictionary(self) -> dict:
        return self.__dict__
    
    @property
    def player_emails_list(self) -> list:
        if type(self.player_emails) == str:
            return [self.player_emails]
        return self.player_emails

    @property
    def parent_class_dict(self) -> dict:
        return {'game_name': self.game_name, 'game_start_ts': self.game_start_ts, 'game_end_ts': self.game_end_ts,
                'player_emails': self.player_emails_list, 'game_data': self.game_data}

    def write_game_to_db(self):
        self.game_end_ts = datetime.utcnow()
        anvil.server.call('write_game_data', self.parent_class_dict)

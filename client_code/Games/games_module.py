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

from ._anvil_designer import LeaderboardRowTemplate
from anvil import *
import anvil.server

from .. import dg_module as m

class LeaderboardRow(LeaderboardRowTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # self.img_player.source = m.get_image_url_from_name(self.lbl_leaderboard_value.text)
    for p in m.dg_players:
      if p['full_name'] == self.lbl_leaderboard_value.text:
        self.img_player.source = p['photo']

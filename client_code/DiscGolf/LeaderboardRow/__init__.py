from ._anvil_designer import LeaderboardRowTemplate
from anvil import *
import anvil.server

from .. import dg_module as m

class LeaderboardRow(LeaderboardRowTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
    
        for p in m.dg_data:
            if p.get('mpo_champion'):
                if p['mpo_champion'] == self.lbl_leaderboard_value.text:
                    self.img_player.source = p['mpo_champ_photo']
                    return
            if p.get('fpo_champion'):
                if p['fpo_champion'] == self.lbl_leaderboard_value.text:
                    self.img_player.source = p['fpo_champ_photo']
                    return

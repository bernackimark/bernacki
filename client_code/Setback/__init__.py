from ._anvil_designer import SetbackTemplate
from anvil import *
from . import SetbackModule as s


class Setback(SetbackTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    

  def play_up_to_show(self, **event_args):
    self.play_up_to.items = []
    for x in [("2", 2), ("3", 3), ("7", 7), ("11", 11), ("15", 15), ("21", 21)]:
      self.play_up_to.items.append(x)
    self.play_up_to.items = self.play_up_to.items

  def create_new_game_click(self, **event_args):
    self.content_panel_new_game.clear()
    self.scores_content_panel.visible = True
    s.this_game.play_up_to = self.play_up_to.selected_value
    
    #self.card1.content = s.p1.hand[0][5]
    #self.card2.content = s.p1.hand[1][5]
    #self.card3.content = s.p1.hand[2][5]
    #self.card4.content = s.p1.hand[3][5]
    #self.card5.content = s.p1.hand[4][5]
    #self.card6.content = s.p1.hand[5][5]
    
    









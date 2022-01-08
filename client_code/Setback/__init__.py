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
    
    self.card1.text = s.p1.hand[0][5]
    self.card2.text = s.p1.hand[1][5]
    self.card3.text = s.p1.hand[2][5]
    self.card4.text = s.p1.hand[3][5]
    self.card5.text = s.p1.hand[4][5]
    self.card6.text = s.p1.hand[5][5]
    
    # BIDDING
    if not s.p1.dealer:  # if the bot is the dealer, human bids then bot bids
      self.show_bid_buttons(-1)
      bot_bid = s.Bot.bid(s.human_bid, s.suggested_bid)
      self.bot_bid_label.text = bot_bid
    else:
      bot_bid = s.Bot.bid(-1, s.suggested_bid)
      self.bot_bid_label.text = bot_bid
      self.show_bid_buttons(bot_bid)
    if human_bid > -1 and bot_bid > -1:
      bid = max(human_bid, bot_bid)
    if bid == human_bid:
        p1.bidder, p2.bidder = True, False
        this_game.update_leader_follower(1, 2)
    else:
        p1.bidder, p2.bidder = False, True
        this_game.update_leader_follower(2, 1)

  def show_bid_panel(self):
    self.bid_panel.visible = True

  def hide_bid_panel(self):
    self.bid_panel.visible = False
  
  def show_bid_buttons(self, bot_bid):
    if s.suggested_bid == 0:
      self.bid0.visible = False
    if s.suggested_bid == 2:
      self.bid2.visible == False
    if s.suggested_bid == 3:
      self.bid2.visible = False
      self.bid3.visible = False
    if s.suggested_bid == 4:
      self.bid2.visible = False
      self.bid3.visible = False
      self.bid4.visible = False

  def bid0_click(self, **event_args):
    human_bid = 0

  def bid2_click(self, **event_args):
    human_bid = 2

  def bid3_click(self, **event_args):
    human_bid = 3

  def bid4_click(self, **event_args):
    human_bid = 4

  def card1_click(self, **event_args):
    # will need to figure out how to handle if we are leading or following
    if s.this_round.turn == 1:
      if s.p1.play_card(s.p1.hand[0][5]):
        self.legit_label.text = "Yes, card is legit"
        if this_round.trick_id == 1:
              this_game.trump = Player.declare_trump(s.p1.hand[0][5])
        p2.play_card_random(this_game.trump, s.p1.hand[0][5])
        
        
      else:
        self.legit_label.text = "No, not valid"
    
  def card2_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def card3_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def card4_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def card5_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def card6_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
  


















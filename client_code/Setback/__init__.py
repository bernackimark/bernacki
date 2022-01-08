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
    
    print(s.p1.hand[0][4], s.p1.hand[1][4], s.p1.hand[2][4], s.p1.hand[3][4], s.p1.hand[4][4], s.p1.hand[5][4])
    print(s.p2.hand[0][4], s.p2.hand[1][4], s.p2.hand[2][4], s.p2.hand[3][4], s.p2.hand[4][4], s.p2.hand[5][4])
    
    # an alternate way to create a UI component from the code
    self.hand = {}
    gp = GridPanel()
    for i in range(len(s.p1.hand)):
      self.hand[i] = Button(text=s.p1.hand[i][5], font_size=200)
      gp.add_component(self.hand[i], row='A', col_xs=3, width_xs=1)
    self.add_component(gp)
    
    # show bid buttons
    if s.this_round.dealer == 2:  # bot is the dealer
      self.show_bid_buttons(-1)
    else:  # human is dealer
      bot_bid = s.Bot.bid(-1, s.suggested_bid)
      self.bot_bid_label.text = bot_bid
      self.show_bid_buttons(bot_bid)

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
    bot_bid = s.Bot.bid(human_bid, s.suggested_bid)
    self.bot_bid_label.text = bot_bid
    self.bidding_eval(human_bid, bot_bid)

  def bid2_click(self, **event_args):
    human_bid = 2
    bot_bid = s.Bot.bid(human_bid, s.suggested_bid)
    self.bot_bid_label.text = bot_bid
    self.bidding_eval(human_bid, bot_bid)

  def bid3_click(self, **event_args):
    human_bid = 3
    bot_bid = s.Bot.bid(human_bid, s.suggested_bid)
    self.bot_bid_label.text = bot_bid
    self.bidding_eval(human_bid, bot_bid)

  def bid4_click(self, **event_args):
    human_bid = 4
    bot_bid = s.Bot.bid(human_bid, s.suggested_bid)
    self.bot_bid_label.text = bot_bid
    self.bidding_eval(human_bid, bot_bid)
  
  def bidding_eval(self, human_bid, bot_bid):
    if human_bid > -1 and bot_bid > -1:
      bid = max(human_bid, bot_bid)
    if bid == human_bid:
        s.p1.bidder, s.p2.bidder = True, False
        s.this_round.update_leader_follower(1, 2)
    else:
        s.p1.bidder, s.p2.bidder = False, True
        s.this_round.update_leader_follower(2, 1)
    print(f"Human bid is {human_bid}. Bot bid is {bot_bid}.")
    self.hide_bid_panel()

  def card1_click(self, **event_args):
    # will need to figure out how to handle if we are leading or following
    if s.this_round.turn == 1:
      if s.p1.play_card(s.p1.hand[0]):
        self.played_cards_panel.add_component(self.hand[0])
        if s.this_round.trick_id == 1:
              s.this_round.trump = s.Player.declare_trump(s.p1.hand[0][5])
        bot_played_card = s.p2.play_card_random(s.this_round.trump, s.p1.hand[0][5]) 
        self.played_cards_panel.add_component(Label(text=bot_played_card[5]))
      else:
        print("Not a valid selection")
    else:
      bot_played_card = s.p2.play_card_random(s.this_round.trump, '')
      if s.this_round.trick_id == 1:
        s.this_round.trump = s.Player.declare_trump(bot_played_card)
      s.this_round.turn = 1
      if s.this_round.turn == 1:
        if s.p1.play_card(s.p1.hand[0]):
          self.played_cards_panel.add_component(self.hand[0])
        else:
          print("Not a valid selection")
    
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
  


















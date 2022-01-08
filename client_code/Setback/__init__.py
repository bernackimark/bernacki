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
    
    print(s.p1.hand[0][4], s.p1.hand[1][4], s.p1.hand[2][4], s.p1.hand[3][4], s.p1.hand[4][4], s.p1.hand[5][4])
    print(s.p2.hand[0][4], s.p2.hand[1][4], s.p2.hand[2][4], s.p2.hand[3][4], s.p2.hand[4][4], s.p2.hand[5][4])
    
    # create a UI component from the code
    self.hand = {}
    for i in range(len(s.p1.hand)):
      self.hand[i] = Button(text=s.p1.hand[i][5], font_size=180, width=140)
      self.hand[i].tag.card_id = s.p1.hand[i][0]
      self.hand[i].tag.rank_id = s.p1.hand[i][1]
      self.hand[i].tag.rank = s.p1.hand[i][2]
      self.hand[i].tag.suit = s.p1.hand[i][3]
      self.hand[i].tag.rank_suit = s.p1.hand[i][4]
      self.hand[i].tag.card_image = s.p1.hand[i][5]
      self.hand[i].set_event_handler('click', self.click)
      self.card_panel.add_component(self.hand[i])
    
    self.bid_panel.visible = False
    
    # show bid buttons
    if s.this_round.dealer == 2:  # bot is the dealer
      self.bid_panel.visible = True
      self.show_bid_buttons(-1)  # show bid buttons, then await human bid, call bot bid there
    else:  # human is dealer
      s.this_round.bot_bid = s.Bot.bid(-1, s.suggested_bid)  # call the bot bid now
      self.bot_bid_label.text = s.this_round.bot_bid
      self.bid_panel.visible = True
      self.show_bid_buttons(s.this_round.bot_bid)

  def click(self, **event_args):
    print(event_args['sender'].tag.card_id)
    for i in range(len(s.p1.hand)):
      if event_args['sender'].tag.card_id == s.p1.hand[i][0]:
        clicked_card = s.p1.hand[i]
        print(clicked_card)
    if s.this_round.turn == 1:
      card_is_legit, p1_played_card = s.p1.play_card(clicked_card)
      if card_is_legit:
        print(p1_played_card[4])
        self.played_cards_label.text += p1_played_card[4]
        if s.this_round.trick_id == 1:
              s.this_round.trump = s.Player.declare_trump(p1_played_card)
              print(f"Trump is {s.this_round.trump}.")
        p2_played_card = s.p2.play_card_random(s.this_round.trump, p1_played_card) 
        print(p2_played_card[4])
        self.played_cards_label.text += p2_played_card[4]
      else:
        print("Not a valid selection")
    else:
      p2_played_card = s.p2.play_card_random(s.this_round.trump, '')
      print(p2_played_card[4])
      self.played_cards_label.text += p2_played_card[4]
      if s.this_round.trick_id == 1:
        s.this_round.trump = s.Player.declare_trump(p2_played_card)
        print(f"Trump is {s.this_round.trump}.")        
      s.this_round.turn = 1
      if s.this_round.turn == 1:
        card_is_legit, p1_played_card = s.p1.play_card(clicked_card)
        if card_is_legit:
          print(p1_played_card[4])
          self.played_cards_label.text += p1_played_card[4]
        else:
          print("Not a valid selection")
      
  def show_bid_buttons(self, bot_bid):
      bot_bid = s.this_round.bot_bid
      print(f"Bot bid is {bot_bid}")
      self.bid_buttons = {}
      bid_options_dict = {-1: [0, 2, 3, 4], 0: [2, 3, 4], 2: [0, 3, 4], 3: [0, 4], 4: [0]}
      i = 0
      for key, value in bid_options_dict.items():
          if bot_bid == key:
              for value_item in value:
                  self.bid_buttons[i] = Button(width=80, role='secondary-color')
                  if value_item == 0:
                    self.bid_buttons[i].text = "Pass"
                  else:
                    self.bid_buttons[i].text = "Bid " + str(value_item)
                  self.bid_buttons[i].tag.bid = value_item
                  # this row was the problem, can't call it "click", because that's already used
                  # having trouble calling it anything else
                  self.bid_buttons[i].set_event_handler('click', self.bid_click)
                  self.bid_panel.add_component(self.bid_buttons[i])
                  i += 1

  def bid_click(self, **event_args):
    print(f"Human bid is {event_args['sender'].tag.bid}")
    s.this_round.human_bid = event_args['sender'].tag.bid
    if s.this_round.bot_bid == -1:  # if the bot bid wasn't already done, do that now 
      s.this_round.bot_bid = s.Bot.bid(s.this_round.human_bid, s.suggested_bid)
      self.bot_bid_label.text = s.this_round.bot_bid
    self.bidding_eval()                
                
  def bidding_eval(self):
    if s.this_round.human_bid > -1 and s.this_round.bot_bid > -1:
      bid = max(s.this_round.human_bid, s.this_round.bot_bid)
    if bid == s.this_round.human_bid:
        s.p1.bidder, s.p2.bidder = True, False
        s.this_round.update_leader_follower(1, 2)
        s.this_round.turn = 1
    else:
        s.p1.bidder, s.p2.bidder = False, True
        s.this_round.update_leader_follower(2, 1)
        s.this_round.turn = 2
    print(f"Human bid is {s.this_round.human_bid}. Bot bid is {s.this_round.bot_bid}.")
    self.bid_panel.visible = False
  


















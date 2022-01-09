from ._anvil_designer import SetbackTemplate
from anvil import *
from . import SetbackModule as s

import time

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
    self.content_panel_new_game.visible = False
    self.scores_content_panel.visible = True
    self.played_cards_panel.visible = True
    self.card_panel.visible = True
    s.this_game.play_up_to = self.play_up_to.selected_value
    print(s.p1.hand[0][4], s.p1.hand[1][4], s.p1.hand[2][4], s.p1.hand[3][4], s.p1.hand[4][4], s.p1.hand[5][4])
    print(s.p2.hand[0][4], s.p2.hand[1][4], s.p2.hand[2][4], s.p2.hand[3][4], s.p2.hand[4][4], s.p2.hand[5][4])
    self.bid_panel.visible = False
    self.display_hand()

    # show bid buttons
    if s.this_round.dealer == 2:  # bot is the dealer
      self.bid_panel.visible = True
      self.show_bid_buttons(-1)  # show bid buttons, then await human bid, call bot bid there
    else:  # human is dealer
      s.this_round.bot_bid = s.Bot.bid(-1, s.suggested_bid)  # call the bot bid now
      self.bid_panel.visible = True
      self.show_bid_buttons(s.this_round.bot_bid)

  def display_hand(self, **event_args):
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
  
  def click(self, **event_args):
    for i in range(len(s.p1.hand)):
      if event_args['sender'].tag.card_id == s.p1.hand[i][0]:
        clicked_card = s.p1.hand[i]
    card_is_legit, p1_played_card = s.p1.play_card(clicked_card)
    if card_is_legit:
      self.card_panel.clear()
      self.display_hand()
      self.p1_played_card_button.text = p1_played_card[5]
      print(clicked_card[4])
      if s.this_round.trick_id == 1:
            s.this_round.trump = s.Player.declare_trump(clicked_card)
            print(f"Trump is {s.this_round.trump}.")
      if len(s.this_round.leader_card) > 0 and len(s.this_round.follower_card) > 0:
        s.this_round.trick_eval()
      else:
        p2_played_card = s.p2.play_card_random(s.this_round.trump, s.this_round.leader_card)
        self.p2_played_card_button.text = p2_played_card[5]
        print(p2_played_card[4])
      leader = s.this_round.trick_eval()
      if leader == 1:
        s.p1.pile_cards(s.this_round.leader_card, s.this_round.follower_card)
        s.this_round.update_leader_follower(1, 2)
      else:
        s.p2.pile_cards(s.this_round.leader_card, s.this_round.follower_card)
        s.this_round.update_leader_follower(2, 1)
      # delay before clearing the cards from the center
      time.sleep(1.5)
      self.p1_played_card_button.text, self.p2_played_card_button.text = '', ''
      
      print(f"This round: {s.this_round}")
      s.this_round.increment_trick_id()
      s.this_round.leader_card, s.this_round.follower_card = [], []
      
      if s.this_round.leader == 2 and s.this_round.trick_id < 7:
        p2_played_card = s.p2.play_card_random(s.this_round.trump, '')
        self.p2_played_card_button.text = p2_played_card[5]
        print(p2_played_card[4])
        s.this_round.leader_card = p2_played_card  
      
      if s.this_round.trick_id > 6:
        print("End of Round!")
        p1_bid_points, p2_bid_points = s.this_round.get_bid_points(s.p1.pile, s.p2.pile)
        s.Dealer.clear_the_piles()
        s.Dealer.move_the_deal(s.this_round.dealer)
        line = s.this_game.scoring_process(p1_bid_points, p2_bid_points, s.this_round.bid)
        self.played_cards_label.text += line
        self.update_score()
        game_over, the_winner, line = s.this_game.did_someone_win()
        if game_over:
          self.played_cards_label.text += line
          
          self.played_cards_panel.visible = False
          self.scores_content_panel.visible = False
          self.content_panel_new_game.visible = True
          # how can i create a new game in the Module code?
          # placing creation of p1, p2, this_game, this_round made those objects unreachable
          # s.create_new_game()
          
        
    
  def update_score(self):
    self.player_score_label.content = s.p1.points
    self.bot_score_label.content = s.p2.points
      
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
    self.bidding_eval()                
                
  def bidding_eval(self):
    if s.this_round.human_bid > -1 and s.this_round.bot_bid > -1:
      s.this_round.bid = max(s.this_round.human_bid, s.this_round.bot_bid)
    if s.this_round.bid == s.this_round.human_bid:
        s.p1.bidder, s.p2.bidder = True, False
        s.this_round.update_leader_follower(1, 2)
        s.this_round.leader = 1
        print(f"Human bid is {s.this_round.human_bid}. Bot bid is {s.this_round.bot_bid}.")
    else:
        s.p1.bidder, s.p2.bidder = False, True
        s.this_round.update_leader_follower(2, 1)
        s.this_round.leader = 2
        print(f"Human bid is {s.this_round.human_bid}. Bot bid is {s.this_round.bot_bid}.")
        p2_played_card = s.p2.play_card_random('','')
        self.p2_played_card_button.text = p2_played_card[5]
        print(p2_played_card[4])
        s.this_round.trump = s.Player.declare_trump(p2_played_card)
        print(f"Trump is {s.this_round.trump}.")
        
    self.bid_panel.visible = False
  


















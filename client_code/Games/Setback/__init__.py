from ._anvil_designer import SetbackTemplate
from anvil import *
import anvil.server
from . import SetbackModule as s

from datetime import datetime
import time

class Setback(SetbackTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.create_game()
    
    self.bot_score.spacing_below = -10
    self.bot_score.spacing_above = -10
    self.human_score.spacing_above = -10
    self.human_score.spacing_below = -10
  
  def create_game(self):
    # can the bot intances go here or would that shield them as variables?
    s.this_game.play_up_to = 11
    self.playing_to.content = "Playing to " + str(s.this_game.play_up_to)
    self.start_round()
  
  def start_round(self):
    s.Dealer.assign_starting_dealer_position()
    s.reset_round()
    self.bid_panel.clear()
    # SHUFFLE & DEAL
    s.deck = s.Dealer.shuffle()
    s.Dealer.deal(6)
    
    s.suggested_bid = 2
    
    if s.this_round.dealer == 2:
      self.ui_display_status('Dealer is bot')
    else:
      self.ui_display_status('Dealer is human')

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
      self.hand[i] = Link(text=s.p1.hand[i][5], font_size=180, width=140, foreground="DDD")
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
      self.p1_played_card_link.text = p1_played_card[5]
      print(clicked_card[4])
      if s.this_round.trick_id == 1:
        s.this_round.trump = s.Player.declare_trump(clicked_card)
        self.ui_display_status(f'Trump is {s.this_round.trump}.')
      if len(s.this_round.leader_card) > 0 and len(s.this_round.follower_card) > 0:
        s.this_round.trick_eval()
      else:
        p2_played_card = s.p2.play_card_random(s.this_round.trump, s.this_round.leader_card)
        self.p2_played_card_link.text = p2_played_card[5]
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
      self.p1_played_card_link.text, self.p2_played_card_link.text = '', ''
      
      print(f"This round: {s.this_round}")
      s.this_round.increment_trick_id()
      s.this_round.leader_card, s.this_round.follower_card = [], []
      
      if s.this_round.leader == 2 and s.this_round.trick_id < 7:
        p2_played_card = s.p2.play_card_random(s.this_round.trump, '')
        self.p2_played_card_link.text = p2_played_card[5]
        print(p2_played_card[4])
        s.this_round.leader_card = p2_played_card  
      
      if s.this_round.trick_id > 6:
        self.end_of_round()
  
  def kick_button_click(self, **event_args):
    self.card_panel.clear()
    for i in range(len(s.p1.hand)):
      s.p2.pile.append(s.p1.hand[i])
    for i in range(len(s.p2.hand)):
      s.p2.pile.append(s.p2.hand[i])
    s.this_round.leader_card, s.this_round.follower_card = [], []
    self.end_of_round()
  
  def end_of_round(self):
    self.ui_display_status('End of Round!')
    print(s.p1.pile, s.p2.pile)
    p1_bid_points, p2_bid_points = s.this_round.get_bid_points(s.p1.pile, s.p2.pile)
    self.kick_button.visible = False
    s.Dealer.clear_the_piles()
    s.Dealer.move_the_deal()
    self.ui_display_status(f"Bid was {s.this_round.bid}. Human bid points: {p1_bid_points}. Bot bid points: {p2_bid_points}.")
    line = s.this_game.scoring_process(p1_bid_points, p2_bid_points, s.this_round.bid)
    self.update_score()
    game_over, the_winner, line = s.this_game.did_someone_win()
    if game_over:      
      s.reset_p1(), s.reset_p2(), s.reset_game(), s.reset_round()
      self.bid_panel.clear()
      self.played_cards_panel.visible = False
    else:
      self.start_round()
    
  def update_score(self):
    self.human_score.content = s.p1.points
    self.bot_score.content = s.p2.points
      
  def show_bid_buttons(self, bot_bid):
      bot_bid = s.this_round.bot_bid
      if s.this_round.dealer == 1:
        self.ui_display_status(f'Bot bid is {bot_bid}')
      self.bid_buttons = {}
      bid_options_dict = {-1: [0, 2, 3, 4], 0: [2, 3, 4], 2: [0, 3, 4], 3: [0, 4], 4: [0]}
      i = 0
      for key, value in bid_options_dict.items():
          if bot_bid == key:
              for value_item in value:
                  self.bid_buttons[i] = Button(width=80, role='secondary-color')
                  if value_item == 0:
                    self.bid_buttons[i].text = "  Pass  "
                  else:
                    self.bid_buttons[i].text = "  Bid " + str(value_item) + "  "
                  self.bid_buttons[i].tag.bid = value_item
                  # this row was the problem, can't call it "click", because that's already used
                  # having trouble calling it anything else
                  self.bid_buttons[i].set_event_handler('click', self.bid_click)
                  self.bid_panel.add_component(self.bid_buttons[i])
                  i += 1

  def bid_click(self, **event_args):
    self.ui_display_status(f"Human bid is {event_args['sender'].tag.bid}")
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
        self.ui_display_status(f"Human bid is {s.this_round.human_bid}. Bot bid is {s.this_round.bot_bid}.")
    else:
        s.p1.bidder, s.p2.bidder = False, True
        s.this_round.update_leader_follower(2, 1)
        s.this_round.leader = 2
        self.ui_display_status(f"Human bid is {s.this_round.human_bid}. Bot bid is {s.this_round.bot_bid}.")
        p2_played_card = s.p2.play_card_random('','')
        self.p2_played_card_link.text = p2_played_card[5]
        print(p2_played_card[4])
        s.this_round.trump = s.Player.declare_trump(p2_played_card)
        self.ui_display_status(f"Trump is {s.this_round.trump}.")
        
    self.bid_panel.visible = False
    self.kick_button.visible = True
    self.kick_button.width, self.kick_spacer.width = 80, 80

  def ui_display_status(self, msg):
    self.info_lbl.text = msg
    for _ in range(3):
      time.sleep(0.05)
      self.info_lbl.foreground = 'white'
      time.sleep(0.15)
      self.info_lbl.foreground = '#F57C00'
      time.sleep(0.25)
      
    


  


















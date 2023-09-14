import random

deck_unshuffled = [[1, 1, '2', 'hearts', '2h', '🂲'], [2, 2, '3', 'hearts', '3h', '🂳'], [3, 3, '4', 'hearts', '4h', '🂴'],
    [4, 4, '5', 'hearts', '5h', '🂵'], [5, 5, '6', 'hearts', '6h', '🂶'], [6, 6, '7', 'hearts', '7h', '🂷'],
    [7, 7, '8', 'hearts', '8h', '🂸'], [8, 8, '9', 'hearts', '9h', '🂹'], [9, 9, 'T', 'hearts', 'Th', '🂺'],
    [10, 10, 'J', 'hearts', 'Jh', '🂻'], [11, 11, 'Q', 'hearts', 'Qh', '🂽'], [12, 12, 'K', 'hearts', 'Kh', '🂾'],
    [13, 13, 'A', 'hearts', 'Ah', '🂱'], [14, 1, '2', 'clubs', '2c', '🃒'], [15, 2, '3', 'clubs', '3c', '🃓'],
    [16, 3, '4', 'clubs', '4c', '🃔'], [17, 4, '5', 'clubs', '5c', '🃕'], [18, 5, '6', 'clubs', '6c', '🃖'],
    [19, 6, '7', 'clubs', '7c', '🃗'], [20, 7, '8', 'clubs', '8c', '🃘'], [21, 8, '9', 'clubs', '9c', '🃙'],
    [22, 9, 'T', 'clubs', 'Tc', '🃚'], [23, 10, 'J', 'clubs', 'Jc', '🃛'], [24, 11, 'Q', 'clubs', 'Qc', '🃝'],
    [25, 12, 'K', 'clubs', 'Kc', '🃞'], [26, 13, 'A', 'clubs', 'Ac', '🃑'], [27, 1, '2', 'diamonds', '2d', '🃂'],
    [28, 2, '3', 'diamonds', '3d', '🃃'], [29, 3, '4', 'diamonds', '4d', '🃄'], [30, 4, '5', 'diamonds', '5d', '🃅'],
    [31, 5, '6', 'diamonds', '6d', '🃆'], [32, 6, '7', 'diamonds', '7d', '🃇'], [33, 7, '8', 'diamonds', '8d', '🃈'],
    [34, 8, '9', 'diamonds', '9d', '🃉'], [35, 9, 'T', 'diamonds', 'Td', '🃊'], [36, 10, 'J', 'diamonds', 'Jd', '🃋'],
    [37, 11, 'Q', 'diamonds', 'Qd', '🃍'], [38, 12, 'K', 'diamonds', 'Kd', '🃎'], [39, 13, 'A', 'diamonds', 'Ad', '🃁'],
    [40, 1, '2', 'spades', '2s', '🂢'], [41, 2, '3', 'spades', '3s', '🂣'], [42, 3, '4', 'spades', '4s', '🂤'],
    [43, 4, '5', 'spades', '5s', '🂥'], [44, 5, '6', 'spades', '6s', '🂦'], [45, 6, '7', 'spades', '7s', '🂧'],
    [46, 7, '8', 'spades', '8s', '🂨'], [47, 8, '9', 'spades', '9s', '🂩'], [48, 9, 'T', 'spades', 'Ts', '🂪'],
    [49, 10, 'J', 'spades', 'Js', '🂫'], [50, 11, 'Q', 'spades', 'Qs', '🂭'], [51, 12, 'K', 'spades', 'Ks', '🂮'],
    [52, 13, 'A', 'spades', 'As', '🂡']]


class Game:
    def __init__(self, game_id, play_up_to, desired_hands, hand_id):
        self.game_id = game_id
        self.play_up_to = play_up_to
        self.desired_hands = desired_hands  # only needed in bot v bot simulations
        self.hand_id = hand_id  # only used right now in bot v bot simulations

    def reset_trick_count(self):
        self.trick_number = 0
        
    @staticmethod
    def scoring_process(p1_bid_p, p2_bid_p, bid):
        # give out the granny points
        if p1.bidder:
            p2.points += p2_bid_p
            line_2 = str(p2.name) + " got " + str(p2_bid_p) + " granny points"
        else:
            p1.points += p1_bid_p
            line_2 = str(p1.name) + " got " + str(p1_bid_p) + " granny points"
        # add/subtract the bidder's points
        if p1.bidder and p1_bid_p >= bid:
            p1.points += p1_bid_p
            line_1 = str(p1.name) + " bid " + str(bid) + " and got " + str(p1_bid_p)
        elif p1.bidder and p1_bid_p < bid:
            p1.points -= bid
            line_1 = str(p1.name) + " got set " + str(bid)
        elif p2.bidder and p2_bid_p >= bid:
            p2.points += p2_bid_p
            line_1 = str(p2.name) + " bid " + str(bid) + " and got " + str(p2_bid_p)
        else:
            p2.points -= bid
            line_1 = str(p2.name) + " got set " + str(bid)
        line = line_1 + " " + line_2
        return line
    
    @staticmethod
    def pg_display_score():
      pass
    
    @staticmethod
    def pg_display_round_summary_text():
      pass
    
    @staticmethod
    def did_someone_win():
        if p1.points >= this_game.play_up_to and p1.points > p2.points:
          line = p1.name + " has won!!!"
          return True, p1.name, line
        elif p2.points >= this_game.play_up_to and p2.points > p1.points:
          line = p2.name + " has won!!!"
          return True, p2.name, line
        else:
          return False, "", ""

          
class Round:
    def __init__(self, round_id, trick_id, dealer, trump, leader, follower, leader_card, follower_card, human_bid, bot_bid, bid):
        self.round_id = round_id
        self.trick_id = trick_id
        self.dealer = dealer
        self.trump = trump
        self.leader = leader
        self.follower = follower
        self.leader_card = leader_card
        self.follower_card = follower_card
        self.human_bid = human_bid
        self.bot_bid = bot_bid
        self.bid = bid
    
    def __repr__(self):
      return f"Round ID {self.round_id} Trick ID {self.trick_id} Dealer {self.dealer} Trump {self.trump} Leader {self.leader} Follower {self.follower} Leader Card {self.leader_card} Follower Card {self.follower_card} Human Bid {self.human_bid} Bot Bid {self.bot_bid} Bid {self.bid}"

    def update_leader_follower(self, incoming_leader_value, incoming_follower_value):
        self.leader = incoming_leader_value
        self.follower = incoming_follower_value
    
    def increment_trick_id(self):
        self.trick_id += 1
    
    def trick_eval(self):
        #  a follower can only win a trick two ways: trumping in or following suit w a higher rank
        if this_round.leader_card[3] != self.trump and this_round.follower_card[3] == self.trump:
            return self.follower
        elif this_round.leader_card[3] == this_round.follower_card[3] and this_round.follower_card[1] > this_round.leader_card[1]:
            return self.follower
        else:
            return self.leader
    
    def get_bid_points(self, pile1, pile2):
        p1_bid_p, p2_bid_p, p1_game, p2_game = 0, 0, 0, 0
        # keeping high, low, jack, game separated out, in case i ever want to display who won each
        trump_cards = [[row[1] for row in pile1 for c in row if c == self.trump], [row[1] for row in pile2 for c in row if c == self.trump]]
        h1, (high_player, h2) = max((x, (i, j)) for i, row in enumerate(trump_cards) for j, x in enumerate(row))
        if high_player == 0:
            p1_bid_p += 1
        else:
            p2_bid_p += 1
        l1, (low_player, l2) = min((x, (i, j)) for i, row in enumerate(trump_cards) for j, x in enumerate(row))
        if low_player == 0:
            p1_bid_p += 1
        else:
            p2_bid_p += 1
        j = [10 in list for list in trump_cards]
        if j[0]:
            p1_bid_p += 1
        elif j[1]:
            p2_bid_p += 1
        else:
            pass
        # find game
        p1_game = [10 for _ in pile1 for c in _ if c == 'T'] + [1 for _ in pile1 for c in _ if c == 'J'] + [2 for _ in pile1 for c in _ if c == 'Q'] + [3 for _ in pile1 for c in _ if c == 'K'] + [4 for _ in pile1 for c in _ if c == 'A']
        p2_game = [10 for _ in pile2 for c in _ if c == 'T'] + [1 for _ in pile2 for c in _ if c == 'J'] + [2 for _ in pile2 for c in _ if c == 'Q'] + [3 for _ in pile2 for c in _ if c == 'K'] + [4 for _ in pile2 for c in _ if c == 'A']
        if p1_game > p2_game:
            p1_bid_p += 1
        elif p2_game > p1_game:
            p2_bid_p += 1
        else:
            pass
        return p1_bid_p, p2_bid_p
          
class Dealer:
    @staticmethod
    def shuffle():
        d = deck_unshuffled.copy()
        random.shuffle(d)
        return d
      
    @staticmethod
    def assign_starting_dealer_position():
        a = random.randint(1, 2)
        if a == 1:
          this_round.dealer = 1
        else:
          this_round.dealer = 2

    @staticmethod
    def deal(number_of_cards):
        for i in range(number_of_cards):  # deal out X cards from the bottom of the deck
            if this_round.dealer == 1:
                p2.hand.append(deck[-1])
                deck.pop()
                p1.hand.append(deck[-1])
                deck.pop()
            else:
                p1.hand.append(deck[-1])
                deck.pop()
                p2.hand.append(deck[-1])
                deck.pop()
        # print(p1.hand)
        # print(p2.hand)

    @staticmethod
    def move_the_deal():
        if this_round.dealer == 1:
            this_round.dealer = 2
        else:
            this_round.dealer = 1

    @staticmethod
    def clear_the_piles():
        p1.pile.clear(), p2.pile.clear()
          
          
class Player:
    def __init__(self, player_id, name, seat, dealer, bidder, is_bot, pile, hand, points):
        self.player_id = player_id
        self.name = name
        self.seat = seat
        self.dealer = dealer
        self.bidder = bidder
        self.is_bot = is_bot
        self.pile = pile
        self.hand = hand
        self.points = points

    def pile_cards(self, lead_card, follow_card):
        self.pile.append(lead_card)
        self.pile.append(follow_card)

    @staticmethod
    def declare_trump(lead_card):
        return lead_card[3]

      
class Human(Player):
    @staticmethod
    def bid(current_bid):
        # bid_buttons = pg_bid_boxes(current_bid)
        # b = bid_click_input(bid_buttons)
        #return b
        pass

    def play_card(self, clicked_card):
        if len(this_round.leader_card) == 0:
          self.hand.remove(clicked_card)
          this_round.leader_card = clicked_card
          return True, clicked_card
        else:
          card_is_legit = human_available_cards(self.hand, clicked_card, this_round.trump, this_round.leader_card)
          if card_is_legit:
            self.hand.remove(clicked_card)
            this_round.follower_card = clicked_card
            return True, clicked_card
          return False, ''


class Bot(Player):
    @staticmethod
    def bid(current_bid, suggested_bid):
        if current_bid == -1:
            return suggested_bid
        elif current_bid == 0:
            return 2
        elif current_bid == 4 or suggested_bid == current_bid or suggested_bid < current_bid:
            return 0
        else:
            return current_bid + 1

    def play_card(self, trump, led_card):
        if led_card != '':
            available_cards = bot_find_available_cards(self.hand, led_card, trump)
        else:
            available_cards = self.hand
        r_b, r_c = bot_v_bot_game(3000, available_cards, "return_best_card", led_card)
        played_card = the_suggested_card(r_c)
        # p2.pg_bot_played_card(played_card)
        self.hand.remove(played_card)
        
        return played_card

    def play_card_random(self, trump, led_card):
        if led_card != '':
            available_cards = bot_find_available_cards(self.hand, led_card, trump)
        else:
            available_cards = self.hand
        the_played_card = random.choice(available_cards)
        self.hand.remove(the_played_card)
        if led_card == '':
          this_round.leader_card = the_played_card
        else:
          this_round.follower_card = the_played_card
        return the_played_card


def human_available_cards(hand, clicked_card, trump, led_card):
  available_cards = []
  led_suit = led_card[3]
  if not any(led_suit in x for x in hand):
    return True
  else:
    for i in range(len(hand)):
      if hand[i][3] == led_card[3] or hand[i][3] == trump:
        available_cards.append(hand[i])
    if clicked_card in available_cards:
      return True
    else:
      return False
  
def bot_find_available_cards(playerhand, leader_card, trump):
    available_cards = []
    led_suit = leader_card[3]
    # if the player doesn't have any of the lead card's suit, all cards are available
    if not any(led_suit in x for x in playerhand):
        return playerhand
    # when we get into this following statement, sometimes, when we bring back 3 or 4 available cards,
    # available_cards.append(playerhand[i]) will run thousands of times.  i tested it by adding a counter to the next
    # row.
    else:
        for i in range(len(playerhand)):
            if playerhand[i][3] == leader_card[3] or playerhand[i][3] == trump:
                available_cards.append(playerhand[i])
        return available_cards

def the_suggested_bid(results):
    # level, % need to make a 2, % need to make a 3, % need to make a 4
    agg_matrix = [[1, 80, 85, 90], [2, 70, 75, 80], [3, 60, 70, 75]]
    # this should be an attribute of the Bot !!!!!
    agg_level = 2

    # convert the raw counts into percentages for each bid (2, 3, 4)
    # a numpy array elements must all be the same data type.  integers is the best visual representation
    a1 = [[0 for _ in range(3)] for _ in range(len(results))]
    for i in range(len(results)):
        a1[i][0] = round(results[i][4] / results[i][1] * 100, 0)  # two bid made %
        a1[i][1] = round(results[i][5] / results[i][1] * 100, 0)  # three bid made %
        a1[i][2] = round(results[i][6] / results[i][1] * 100, 0)  # four bid made %

    a2 = [[0, 0, 0], [0, 0, 0]]
    # find the maximum make % for each bid
    a2[1][0] = np.amax(a1, axis=0)[0]
    a2[1][1] = np.amax(a1, axis=0)[1]
    a2[1][2] = np.amax(a1, axis=0)[2]

    # for the given aggression level, find the minimum % needed for each bid
    for i in range(len(agg_matrix)):
        if agg_matrix[i][0] == agg_level:
            a2[0][0] = agg_matrix[i][1]
            a2[0][1] = agg_matrix[i][2]
            a2[0][2] = agg_matrix[i][3]

    # if there is a make % >= what is needed for the aggression level, return that bid. highest bid gets preference.
    if a2[1][2] >= a2[0][2]:
        s_bid = 4
    elif a2[1][1] >= a2[0][1]:
        s_bid = 3
    elif a2[1][0] >= a2[0][0]:
        s_bid = 2
    else:
        s_bid = 0

    return s_bid

def the_suggested_card(results):
    a1 = [0, 0]
    for i in range(len(results)):
        row_to_insert = [0, 0]
        a1 = np.vstack([a1, row_to_insert])
    # delete the dummy temp first row
    a1 = np.delete(a1, 0, 0)

    for i in range(len(results)):
        a1[i][0] = results[i][0]
        # this is the net of good bot and other bot's points, it emphasizes the more optimal played card
        # we always want the best net
        a1[i][1] = round((results[i][2] - results[i][3]) / results[i][1], 3) * 100

    for i in range(len(results)):
        if a1[i][1] == np.amax(a1, axis=0)[1]:
            suggested_card_id = a1[i][0]

    # print(a1)

    # from the card ID, get the entire card
    for i in range(len(deck_unshuffled)):
        if suggested_card_id == deck_unshuffled[i][0]:
            suggested_card = deck_unshuffled[i]

    return suggested_card

def reset_p1():
  p1.dealer, p1.bidder, p1.pile, p1.hand, p1.points = False, False, [], [], 0

def reset_p2():
  p2.dealer, p2.bidder, p2.pile, p2.hand, p2.points = False, False, [], [], 0

# don't we want a new game instead of a game reset???!!!  
def reset_game():
  this_game.game_id, this_game.play_up_to, this_game.desired_hands, this_gamehand_id = 0, 7, -1, 0

def reset_round(): # resetting the round doesn't -- and shouldn't -- reset the dealer button
  this_round.round_id, this_round.trick_id, this_round.trump, this_round.leader, this_round.follower, this_round.leader_card, this_round.follower_card, this_round.human_bid, this_round.bot_bid, this_round.bid = 0, 1, '', -1, -1, [], [], -1, -1, -1
  
  
  
# need these to be at the main-level to start the game  
p1 = Human(1, "Mark", 1, False, False, False, [], [], 0)
p2 = Bot(2, "Ackerman", 2, False, False, True, [], [], 0)
this_game = Game(0, 7, -1, 0)  # game id, play up to, desired hands, hand id
this_round = Round(0, 1, -1, '', -1, -1, [], [], -1, -1, -1) # round ID, trick ID, dealer, trump, turn, l, f, l card, f card, human bid, b bid, bid
          

# -- send the hand to the Bot Algorithm and get back the suggested bid
# rb, rc = bot_v_bot_game(3000, p2.hand, aim="return_a_bid", led_card='')
# suggested_bid = the_suggested_bid(rb)





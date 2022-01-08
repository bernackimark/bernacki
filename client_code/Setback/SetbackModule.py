# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

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
    def __init__(self, play_up_to, desired_hands, hand_id, trick_number, leader, follower, trump):
        self.play_up_to = play_up_to
        self.desired_hands = desired_hands  # only needed in bot v bot simulations
        self.hand_id = hand_id  # only used right now in bot v bot simulations
        self.trick_number = trick_number
        self.leader = leader
        self.follower = follower
        self.trump = trump

    def reset_trick_count(self):
        self.trick_number = 0

    def increment_trick_number(self):
        self.trick_number += 1
        return self.trick_number

    def trick_eval(self, the_leader, the_follower):
        #  a follower can only win a trick two ways: trumping in or following suit w a higher rank
        if the_leader[3] != self.trump and the_follower[3] == self.trump:
            return self.follower
        elif the_leader[3] == the_follower[3] and the_follower[1] > the_leader[1]:
            return self.follower
        else:
            return self.leader

    def update_leader_follower(self, incoming_leader_value, incoming_follower_value):
        self.leader = incoming_leader_value
        self.follower = incoming_follower_value

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

    def reset_trick_leader(self):
        self.leader = 0
        self.follower = 0   
        
    @staticmethod
    def scoring_process(p1_bid_p, p2_bid_p, b):
        # give out the granny points
        if p1.bidder:
            p2.points += p2_bid_p
            line_2 = str(p2.name) + " got " + str(p2_bid_p) + " granny points"
        else:
            p1.points += p1_bid_p
            line_2 = str(p1.name) + " got " + str(p1_bid_p) + " granny points"
        # add/subtract the bidder's points
        if p1.bidder and p1_bid_p >= b:
            p1.points += p1_bid_p
            line_1 = str(p1.name) + " bid " + str(b) + " and got " + str(p1_bid_p)
        elif p1.bidder and p1_bid_p < b:
            p1.points -= b
            line_1 = str(p1.name) + " got set " + str(b)
        elif p2.bidder and p2_bid_p >= b:
            p2.points += p2_bid_p
            line_1 = str(p2.name) + " bid " + str(b) + " and got " + str(p2_bid_p)
        else:
            p2.points -= b
            line_1 = str(p2.name) + " got set " + str(b)
        return line_1, line_2
    
    @staticmethod
    def pg_display_score():
      pass
    
    @staticmethod
    def pg_display_round_summary_text():
      pass
    
    @staticmethod
    def did_someone_win(play_up_to):
        if p1.points >= play_up_to and p1.points > p2.points:
            return True, p1.name
        elif p2.points >= play_up_to and p2.points > p1.points:
            return True, p2.name
        else:
            return False, ""

          
class Dealer:
    @staticmethod
    def assign_starting_dealer_position():
        a = random.randint(1, 2)
        return a

    @staticmethod
    def assign_deal(dealer_b_position):
        if dealer_b_position == p1.seat:
            dealer_b_position = 1
            p1.dealer = True
            p2.dealer = False
        else:
            dealer_b_position = 2
            p1.dealer = False
            p2.dealer = True
        return dealer_b_position

    @staticmethod
    def pg_draw_dealer_button(dealer_b_position):
        pass

    @staticmethod
    def shuffle():
        d = deck_unshuffled.copy()
        random.shuffle(d)
        return d

    @staticmethod
    def deal(number_of_cards, dealer_b_position):
        for i in range(number_of_cards):  # deal out X cards from the bottom of the deck
            if dealer_b_position == p1.seat:
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
    def move_the_deal(dealer_b_position):
        if dealer_b_position == 1:
            return 2
        else:
            return 1

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
        bid_buttons = pg_bid_boxes(current_bid)
        b = bid_click_input(bid_buttons)
        return b

    def play_leader_card(self):
        played_card = pg_card_click_input(self.hand, this_game.trump, led_card='')
        self.hand.remove(played_card)
        # pg_display_hand(self.hand, this_game.trick_number)
        return played_card

    def play_follower_card(self, led_card):
        played_card = pg_card_click_input(self.hand, this_game.trump, led_card)
        self.hand.remove(played_card)
        # pg_display_hand(self.hand, this_game.trick_number)
        return played_card


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
        random_card_index = random.randint(0, len(available_cards) - 1)
        the_played_card = available_cards[random_card_index]
        self.hand.remove(the_played_card)
        return the_played_card

      
p1 = Human(1, "Mark", 1, False, False, False, [], [], 0)
p2 = Bot(2, "Ackerman", 2, False, False, True, [], [], 0)
this_game = Game(7, -1, 0, 0, 0, 0, '')  # play up to, desired hands, hand id, t number, t leader, t follower, trump
game_over = False
dealer_button_position = Dealer.assign_starting_dealer_position()

while not game_over:
    # SHUFFLE & DEAL
    deck = Dealer.shuffle()

    dealer_button_position = Dealer.assign_deal(dealer_button_position)
    Dealer.pg_draw_dealer_button(dealer_button_position)
    Dealer.deal(6, dealer_button_position)
    # pg_display_hand(p1.hand, trick_number=0)
    this_game.reset_trick_leader()

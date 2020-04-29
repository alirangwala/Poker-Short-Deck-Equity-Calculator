from itertools import combinations
from collections import Counter
import random
import time
# Constants
value_dict = {"6": 6,"7":7 , "8":8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
suit_index_dict = {"s": 0, "c": 1, "h": 2, "d": 3}
val_string = "AKQJT9876"

class Card:
    # Takes in strings of the format: "As", "Tc", "6d"
    def __init__(self, card_string):
        self.value = value_dict[card_string[0]]
        self.suit = card_string[1]

    def __str__(self):
        return val_string[14 - self.value] + self.suit

    def __repr__(self):
        return val_string[14 - self.value] + self.suit

    def __eq__(self, other):
        if self is None:
            return other is None
        elif other is None:
            return False
        return self.value == other.value and self.suit == other.suit


def generate_deck(exp_cards=[]):
    deck = []
    for value in value_dict:
        for suit in suit_index_dict:
            deck.append(Card(value + suit))
    # remove hole cards and board card_string
    # set exposed cards to whatever is on the board  and in hands at the moment
    for card in exp_cards:
        deck.remove(card)
    return(deck)

# Takes in number of sims wanted and cards exposed and combines them
def random_boards(exp_cards, num_iter, board = []):
    deck = generate_deck(exp_cards)
    num_cards = len(board)
    random.seed(time.time())
    for i in range(num_iter):
        yield random.sample(deck, 5 - num_cards)

# Generate all possible boards
def generate_all_boards(exp_cards, board = []):
    deck = generate_deck(exp_cards)
    num_cards = len(board)
    return combinations(deck, 5 - num_cards)

# Note all the definitions are not perfect. They just need to exclude all the lower rankings.
# For example High Card returns a list of the 5 highest cards even if they are the same
# In the comparison function we will have a pair hand take over instead of high card by order in

# Check for straight flush inside the detect flush to make code simpler
def detect_flush(board):
    board_suits = [board[i].suit for i in range(len(board))]
    occurence_count = Counter(board_suits)
    suit_occur = Counter.most_common(occurence_count)[0][1]
    if suit_occur < 5:
        return False
    else:
        suit = Counter.most_common(occurence_count)[0][0]
        suited_vals = sorted([board[i].value for i in range(len(board)) if board[i].suit == suit], reverse = True)
        if all(x in suited_vals for x in [i for i in range(min(suited_vals),max(suited_vals)-1)]):
            return "Straight Flush", max(suited_vals)
            # Return Straight Flush and high end value value
        else:
            return "Flush", suited_vals[0], suited_vals[1], suited_vals[2], suited_vals[3], suited_vals[4]
            # Return Flush and five highest suited cards

def detect_straight(board):
    sorted_board = [board[i].value for i in range(len(board))]
        #Start with Highest Straight (Broadway)
    if all(x in sorted_board for x in [10, 11, 12, 13, 14]):
        return "Straight", 14
    elif all(x in sorted_board for x in [9, 10, 11, 12, 13]):
        return "Straight", 13
    elif all(x in sorted_board for x in [8, 9, 10, 11, 12]):
        return "Straight", 12
    elif all(x in sorted_board for x in [7, 8, 9, 10, 11]):
        return "Straight", 11
    elif all(x in sorted_board for x in [6, 7, 8, 9, 10]):
        return "Straight", 10
        #Account for Ace as low card
    elif all(x in sorted_board for x in [14, 6, 7, 8, 9]):
        return "Straight", 9
    else:
         return False
         # Return Straight and high end value

# Use this function for Pair, Two Pair, Three of a Kind, Full House and Four of a Kind
# create a dictionary {value: value frequency} Ex. Pair of Ace {0: 2} Quad 6s {8: 4}
# cards are reversed so you can iterate from high to low
# Note these values are ranked on a different scale as the original: 0-8 instead of 6-14.
# It won't matter as only the same rakings will be compared for tiebreaks
def freq_board(board):
    histogram = [0] * 9
    for card in board:
        histogram[14 - card.value] += 1
    return histogram[::-1]

def detect_four_of_a_kind(board):
    # Four of a kind if exactly one foursome
    freq = freq_board(board)
    if any(card == 4 for card in freq):
        kicker = list(map(lambda i: i> 0 and i !=4, freq)).index(True)
        return "Four of a Kind", freq.index(4), kicker
    else:
        return False

def detect_full_house(board):
    # Full house if 3 of a kind and pair or multiple 3 of a kinds
    freq = freq_board(board)
    if any(card == 4 for card in freq):
        return False
    elif any(card == 3 for card in freq) and any(card == 2 for card in freq):
        high_pair = list(map(lambda i: i == 2, freq)).index(True)
        return "Full House", freq.index(3), high_pair
    elif freq.count(3) == 2:
        high_trip = list(map(lambda i: i == 3, freq)).index(True)
        freq[high_trip] = 0
        second_trip =list(map(lambda i: i == 3, freq)).index(True)
        return "Full House", high_trip, second_trip
    else:
        return False

def detect_three_of_a_kind(board):
    freq = freq_board(board)
    # Three of a kind if exactly one threesome
    if any(card == 2 for card in freq):
        return False
    elif any(card == 4 for card in freq):
        return False
    elif freq.count(3) == 1:
        kicker = list(map(lambda i: i == 1, freq)).index(True)
        freq[kicker] = 0
        sec_kicker = list(map(lambda i: i == 1, freq)).index(True)
        return "Three of a Kind",  freq.index(3), kicker, sec_kicker
    else:
        return False

def detect_two_pair(board):
    freq = freq_board(board)
    # Two Pair if more than one pair
    if any(card > 2 for card in freq):
        return False
    elif freq.count(2) > 1:
        high_pair = list(map(lambda i: i == 2, freq)).index(True)
        freq[high_pair] = 0
        sec_high_pair = list(map(lambda i: i == 2, freq)).index(True)
        freq[sec_high_pair] = 0
        kicker = list(map(lambda i: i > 0, freq)).index(True)
        return "Two Pair", high_pair, sec_high_pair, kicker
    else:
        return False

def detect_pair(board):
    freq = freq_board(board)
    # Pair if exactly one pair
    if any(card > 2 for card in freq):
        return False
    elif freq.count(2) == 1:
        kicker = list(map(lambda i: i ==1, freq)).index(True)
        freq[kicker] = 0
        sec_kicker = list(map(lambda i: i ==1, freq)).index(True)
        freq[sec_kicker] = 0
        third_kicker = list(map(lambda i: i ==1, freq)).index(True)
        return "Pair", freq.index(2), kicker, sec_kicker, third_kicker
    else:
        return False

def detect_high_card(board):
    vals = sorted([board[i].value for i in range(len(board))], reverse = True)[:5]
    freq = freq_board(board)
    if any(card > 1 for card in freq):
        return False
    else:
        board_list = [board[i].value for i in range(len(board))]
        return "High Card", vals

# Return results in lists that can be easily compared
def detect_triton_hand(board):
    #first detect straight flush
    if detect_flush(board) != False and detect_flush(board)[0] == "Straight Flush":
        strflush = (list(detect_flush(board)[1:]))
        strflush.insert(0,8)
        return strflush
    elif detect_four_of_a_kind(board) != False:
        fourkind = (list(detect_four_of_a_kind(board)[1:]))
        fourkind.insert(0,7)
        return fourkind
    elif detect_flush(board) != False and detect_flush(board)[0] == "Flush":
        flush = (list(detect_flush(board)[1:]))
        flush.insert(0,6)
        return flush
    elif detect_full_house(board) != False:
        fullhouse = (list(detect_full_house(board)[1:]))
        fullhouse.insert(0,5)
        return fullhouse
    elif detect_straight(board) != False:
        straight = (list(detect_straight(board)[1:]))
        straight.insert(0,4)
        return straight
    elif detect_three_of_a_kind(board) != False:
        threekind = (list(detect_three_of_a_kind(board)[1:]))
        threekind.insert(0,3)
        return threekind
    elif detect_two_pair(board) != False:
        twopair = (list(detect_two_pair(board)[1:]))
        twopair.insert(0,2)
        return twopair
    elif detect_pair(board) != False:
        pair = (list(detect_pair(board)[1:]))
        pair.insert(0,1)
        return pair
    elif detect_high_card(board) != False:
        high = (list(detect_high_card(board)[1:]))
        high.insert(0,0)
        return high
    else:
        return "Still Working"

# Ordering and ranking of straight and three of a kind are switched
def detect_sixplus_hand(board):
    #first detect straight flush
    if detect_flush(board) != False and detect_flush(board)[0] == "Straight Flush":
        strflush = (list(detect_flush(board)[1:]))
        strflush.insert(0,8)
        return strflush
    elif detect_four_of_a_kind(board) != False:
        fourkind = (list(detect_four_of_a_kind(board)[1:]))
        fourkind.insert(0,7)
        return fourkind
    elif detect_flush(board) != False and detect_flush(board)[0] == "Flush":
        flush = (list(detect_flush(board)[1:]))
        flush.insert(0,6)
        return flush
    elif detect_full_house(board) != False:
        fullhouse = (list(detect_full_house(board)[1:]))
        fullhouse.insert(0,5)
        return fullhouse
    elif detect_three_of_a_kind(board) != False:
        threekind = (list(detect_three_of_a_kind(board)[1:]))
        threekind.insert(0,4)
        return threekind
    elif detect_straight(board) != False:
        straight = (list(detect_straight(board)[1:]))
        straight.insert(0,3)
        return straight
    elif detect_two_pair(board) != False:
        twopair = (list(detect_two_pair(board)[1:]))
        twopair.insert(0,2)
        return twopair
    elif detect_pair(board) != False:
        pair = (list(detect_pair(board)[1:]))
        pair.insert(0,1)
        return pair
    elif detect_high_card(board) != False:
        high = (list(detect_high_card(board)[1:]))
        high.insert(0,0)
        return high
    else:
        return "Still Working"

# funtion will return a tuple with the first item being the index of the winning
# hand, and the second item being the hand that player 1 (index 0) got
def compare_hands(players_holdings, game):
    if game == "triton":
        player_hands = [detect_triton_hand(hand) for hand in players_holdings]
        max_hand = max(player_hands)
        winning_indices= [i for i in range(len(player_hands)) if player_hands[i] == max_hand ]
        return winning_indices, player_hands[0][0]
    elif game == "sixplus":
        player_hands = [detect_sixplus_hand(hand) for hand in players_holdings]
        max_hand = max(player_hands)
        winning_indices= [i for i in range(len(player_hands)) if player_hands[i] == max_hand ]
        return winning_indices, player_hands[0][0]
    else:
        return "Invalid Game"

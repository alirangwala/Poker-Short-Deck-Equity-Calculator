import os
import argparse
import poker_functions as fp
# choose type of short deck
# Short Deck Poker comes in two versions: Six plus Holdem and a Triton variant
# Triton variant Straight > 3 of a kind
# Six plus Holdem 3 of a Kind > straight

def parse_args():
    # Defining command line arguments
    parser = argparse.ArgumentParser(description= "Calculate your Short Deck odds. Note: Enter cards in this format: As, Qc, Th, 2d")
    parser.add_argument("-b", "--board", nargs="*", type=str, default= list(), metavar="board cards", help="Add board cards")
    parser.add_argument("-c", "--cards", nargs="*", type=str,  metavar="hole cards", help="Add Hole cards")
    parser.add_argument("-n", "--num", type=int, default=0, help="Run n Monte Carlo simulations. Defaults to exact answer")
    parser.add_argument("-g", "--game", type=str, default="triton", help="Triton or original rules")
    args = parser.parse_args()
    check_arg_errors(args)
    return args.game, list(map(fp.Card, args.board)), create_hole_card_tuples(args.cards), args.num

# Argument Error Handling
def check_arg_errors(args):
    # Create list of possible cards for check
    possible_cards = []
    for i in fp.generate_deck():
        possible_cards.append(str(i))
        # Check for card format and that in deck
    if not all(item in possible_cards for item in args.cards):
        print(f"Hole Cards {args.cards} are in an invalid format or are not in the Deck.")
        exit()
    elif not all(item in possible_cards for item in args.board):
            print(f"Board Cards {args.board} are in an invalid format or are not in the Deck.")
            exit()
            # Check no cards are repeated
    elif len((args.cards + args.board)) != len(list(set(args.cards + args.board))):
        print("Hole cards and/or Board cards are not unique")
        exit()
    elif len(args.cards) % 2 != 0:
        print("Must provide an even number of Hole cards")
        exit()
    elif len(args.board) not in [0, 3, 4, 5]:
        print("Must provide either 0, 3, 4, or 5 Board Cards")
        exit()
    elif args.game not in ("triton", "sixplus"):
        print("Enter either 'triton' or 'sixplus'")
        exit()
    else:
        return

def create_hole_card_tuples(args):
    card_args = list(map(fp.Card, args))
    tuples = zip(card_args[0::2], card_args[1::2])
    paired_cards = list(tuples)
    return paired_cards

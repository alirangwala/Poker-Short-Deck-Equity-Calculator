import time
import poker_functions as pf
import interface

triton_hand_rank = ("High Card", "Pair", "Two Pair", "Three of a Kind",
                 "Straight", "Full House", "Flush", "Four of a Kind",
                 "Straight Flush")
sixplus_hand_rank = ("High Card", "Pair", "Two Pair","Straight",
                 "Three of a Kind", "Full House", "Flush", "Four of a Kind",
                 "Straight Flush")

def main():
    GAME, BOARD, HOLE_CARDS, NUM = interface.parse_args()
    return run_sims(HOLE_CARDS, BOARD, GAME, NUM)

# Combine hole cards and board
def cards_and_board(hole_cards, board):
    holdings = []
    i = 0
    while i < len(hole_cards):
        holdings.append(list(hole_cards[i]) + board)
        i += 1
    return holdings

# make a list of all the hole cards and board cards
# These will be exluded from generated cards
def exposed_cards(hole_cards, board):
    exp_hole_cards = list(sum(hole_cards, ())) + board
    return exp_hole_cards

def exhaustive_boards(hole_cards, board):
    all_gen_boards = list(pf.generate_all_boards(exposed_cards(hole_cards, board), board))
    player_holdings = cards_and_board(hole_cards,board)
    all_full_boards = [[] for x in range(len(all_gen_boards))]
    for i in range(len(all_gen_boards)):
        for j in range(len(player_holdings)):
            all_full_boards[i].append(list(all_gen_boards[i]) + player_holdings[j])
    return all_full_boards

def monte_carlo_boards(hole_cards, board, num_iter):
    random_boards = list(pf.random_boards(exposed_cards(hole_cards, board), num_iter, board))
    player_holdings = cards_and_board(hole_cards,board)
    mc_boards = [[] for x in range(len(random_boards))]
    for i in range(len(random_boards)):
        for j in range(len(player_holdings)):
            mc_boards[i].append(list(random_boards[i]) + player_holdings[j])
    return mc_boards

def run_sims(hole_cards, board, game = "triton", num_iter = 0):
    winners = [0] * len(hole_cards)
    player_hands = [0] * 9 # high card through straight flush
    ties = [0] * len(hole_cards)
    if num_iter == 0:
        ex_boards = exhaustive_boards(hole_cards, board)
        for i in range(len(ex_boards)):
            results = pf.compare_hands(ex_boards[i], game)
            player_hands[results[1]] += 1
            if len(results[0]) == 1:
                winners[results[0][0]] += 1
            else:
                for j in range(len(results[0])):
                    ties[results[0][j]] += 1
    else:
        mc_boards = monte_carlo_boards(hole_cards, board, num_iter)
        for i in range(len(mc_boards)):
            results = pf.compare_hands(mc_boards[i], game)
            player_hands[results[1]] += 1
            if len(results[0]) == 1:
                winners[results[0][0]] += 1
            else:
                for j in range(len(results[0])):
                    ties[results[0][j]] += 1
                    
    print('\n')
    print(f"Board: {board}")
    print("Hand Equities:")
    for x in range(len(winners)):
        print(f"Player {x + 1}: {hole_cards[x]} {round((winners[x]/(sum(winners) + sum(ties)/2))*100, 3)} % chance of winning \
        {round((ties[x]/2/(sum(winners) + sum(ties)/2))*100, 3)}% chance of a tie")
    print('\n')
    print("Player 1 Possible Hands:")
    if game == "triton":
        for y in range(len(player_hands)):
            print(f"{triton_hand_rank[y]} {round((player_hands[y]/sum(player_hands))*100, 3)}%")
    else:
        for y in range(len(player_hands)):
            print(f"{sixplus_hand_rank[y]} {round((player_hands[y]/sum(player_hands))*100, 3)}%")
    return "\n"


if __name__ == "__main__":
    start = time.time()
    print(main())
    end = time.time()
    print(f"Done in {round(end - start, 3)} seconds")

What is short deck?

Short deck hold'em is a version of Texas hold'em where the cards below 6 are removed from the deck. This results in a 36 card deck with a lot more action and different hand rankings (Flush beats full house and trips beats straight--in some versions). As the pool of players in Texas Hold'em is becoming dominated by online experts, the game is losing popularity among the amateur. Especially since playing Hold'em optimally requires lots of patience it seems like a more action filled novel version of poker may move in to fill the gap. A game that hasn't been figured out until now!

Who plays short deck?

Short deck is becoming increasingly popular because it is attracting lots of amatuers to the tables. This higher variance game makes it so almost anyone can win in the short term; it takes a a student of the game with an equity calculator to win in the long term. Some of my favorite players including Phil Ivey and Tom Dwan have been popularizing the game overseas in Macau and games are already starting to pop up in Vegas. Soon everyone who's sick of the silent, calculating Texas Hold'em table full of grinders may transition over to this action packed game.

How is this game different than Texas hold'em?

As mentioned earlier cards 2-5 are removed from the deck resulting in a 36 card deck. This does many things like making straights and pairs easier to hit while making flushes tougher. As a result different versions of short deck have different hand rankings. This equity calculator will cover the two most popular: the orginal six plus rankings and the Triton Series hand rankings. The latter has a straight beating three of a kind despite the higher probabilty of hitting a straight.

How do I use this app?

Command Line Inputs:

-b, --board: specify the cards on the board (ie flop, turn, river) 
-c, --cards: specify your hole cards and the hole cards of opponents 
-n, --num: specify the number of Monte Carlo simulations you want to run. Defaults to exact answer (longest run-time) 
-g, --game: specify set of rules either "triton" or "sixplus"

Only input cards in this format: As, Qc, Th, 2d

Example:

python calculator.py -c Ac Ah Js Ts -b 6s 7s 8h -n 10000 -g triton
Board: [6s, 7s, 8h] 
Hand Equities: 
Player 1: (Ac, Ah) 42.53 % chance of winning 2.56% chance of a tie 
Player 2: (Js, Ts) 52.35 % chance of winning 2.56% chance of a tie

Player 1 Possible Hands: High Card 0.0% Pair 18.21% Two Pair 41.31% Three of a Kind 6.97% Straight 26.25% Full House 6.96% Flush 0.0% Four of a Kind 0.3% Straight Flush 0.0%

Done in 7.009 seconds


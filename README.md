# Short Deck Hold'em Equity Calculator

## Why use this software?

This tool is designed to make you a better player by showing you the math behind the game. Ever wonder if you made the right decision on the turn? Should I have called that all in bet? Did I actually have good enough odds to hit that flush on the river? All the answers lie in a single line of code in your command line. By using this app to inspect your hands after a session you will be able to find holes in your game, errors in calculations, or assure yourself of correct calls or folds you made. 

## What is short deck?

Short deck hold'em is a version of Texas hold'em where the cards below 6 are removed from the deck. This results in a 36 card deck with a lot more action and different hand rankings (flush beats full house and trips beats straight--in some versions). As the pool of players in Texas Hold'em is becoming dominated by online experts, the game is losing popularity among the amateur. Short deck is designed to have a lot more action and variance so it is rising to fill the gap. The new game hasn't been figured out until now!

For more information visit <https://triton-series.com/understand-short-deck-holdem/>

## Who plays short deck?

Short deck is becoming increasingly popular because it is attracting lots amateurs to the tables. This higher variance game makes it so almost anyone can win in the short term; it takes a a student of the game with an equity calculator to win in the long term. Some of my favorite players including Phil Ivey and Tom Dwan have been popularizing the game overseas in Macau. Short deck tournaments have also been added to the World Series of Poker tour . Soon everyone who's sick of the silent, calculating Texas Hold'em table full of grinders will transition over to this action packed game.


## Poker terms to know:

  Hole Cards - The two cards held by a player that only that player can see.
  
  Board - The community cards that include the flop, turn, and river.
  
  Flop - First three cards on the board
  
  Turn - Fourth card on the board
  
  River - Fifth and final card on the board. After the river everyone's equity has been realized.
  
  Equity - Odds of winning the pot at any given moment in time.
  
## How do I use this app?

After you download the repository and set up the directory explore the parameters:


```sh
python calculator.py -h


usage: calculator.py [-h] [-b [BOARD [BOARD ...]]] [-c [CARDS [CARDS ...]]]
                     [-n NUM] [-g GAME]

Calculate your Short Deck odds. Be sure to enter cards in this format: As, Qc, Th, 2d

optional arguments:
  -h, --help            show this help message and exit
  -b [BOARD [BOARD ...]], --board [BOARD [BOARD ...]]
                        Add board cards ie flop, turn, river
  -c [CARDS [CARDS ...]], --cards [CARDS [CARDS ...]]
                        Add hole cards
  -n NUM, --num NUM     Run n Monte Carlo simulations. Defaults to exact
                        answer. Monte Carlo simulations will have a lower
                        runtime when there are no board cards.
  -g GAME, --game GAME  Select triton or original rules. Triton rules straight > three of a kind.
```

## Example

```sh
python calculator.py -c As Ah Jd Th -b 6d 8d 9d -n 1000


Board: [6d, 8d, 9d]
Hand Equities:
Player 1: (As, Ah) 29.8 % chance of winning         3.2% chance of a tie
Player 2: (Jd, Th) 63.8 % chance of winning         3.2% chance of a tie


Player 1 Possible Hands:
High Card 0.0%
Pair 16.6%
Two Pair 42.2%
Three of a Kind 5.8%
Straight 25.2%
Full House 7.5%
Flush 2.2%
Four of a Kind 0.1%
Straight Flush 0.4%


Done in 0.122 seconds

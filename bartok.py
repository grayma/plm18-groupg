from starterpack import *
from random import shuffle

#==============================================================================
# Standard Deck
#==============================================================================
suits = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


def get_deck():
    return [Card(value, suit) for value in values for suit in suits]

#==============================================================================
# move functions
#==============================================================================

def play(player, state, input):
    return ""

def draw(player, state, input):
    return ""

def placeholder(player, state, input):
    return ""

#==============================================================================
# moves
#==============================================================================

draw_move = Move("draw", draw, { "Nothing (press enter)" })
play_move = Move("play", play, {"card": None})
placeholder_move = Move("placeholder", placeholder, {})


#==============================================================================
# transition functions
#==============================================================================

def transition_stub(state):
    pass
    
def reset_game(state):
    score_hand(state)
    deck = get_deck()
    shuffle(deck)
    shuffle(deck)
    shuffle(deck)
    state["players"][:] = []
    deal(game.game_state, deck)
    game.game_state["topCard"] = deck.pop()
    game.game_state["deck"] = deck
    game.game_state["discard"] = []
    
def conclude_game(state):
    score_hand(state)
    print("Final Score:")
    [print("%s: %d" % (p.name, p.score)) for p in state["players"]]

#==============================================================================
# transitions
#==============================================================================

# len(state[STATE_PLAYERS][0].hand) == 0 or len(state[STATE_PLAYERS][0].hand) == 0
main_to_main = Transition("main", (lambda state: not any(len(p.hand) == 0 for p in state["players"])), transition_stub)
main_to_main_reset = Transition("start",
       (lambda state: 
            any(len(p.hand) == 0 for p in state["players"]) and get_highest_score(state[STATE_PLAYERS]) < 100),
       reset_game)
main_to_finish = Transition("finish", (lambda state: get_highest_score(state[STATE_PLAYERS]) >= 100), conclude_game)

#==============================================================================
# states
#==============================================================================

main_transitions = [main_to_main_reset, main_to_main, main_to_finish]
main_moves = [play_move, draw_move]
main = State("main", main_transitions, main_moves, game_status, False)

finish = State("finish", None, [placeholder_move], game_status, True)

states = [start, main, finish]

#==============================================================================
# board helpers
#==============================================================================

def game_status(player, state):
    print("\nTurn " + str(state[STATE_TURN]))
    print("Showing %s info about the game." % (player.name))
    printBoard(state)
    print(player.hand)
    print()  # separator line


#==============================================================================
# players
#==============================================================================

players = []
for i in range(1, 5):
    name = input("What is the name of player " + str(i) + "? ")
    hand = []
    player = Player(name, {}, i, hand, 0)
    players.append(player)


#==============================================================================
# setup/finish
#==============================================================================

def setup(game):
    deck = get_deck()
    shuffle(deck)
    shuffle(deck)
    shuffle(deck)
    deal(game.game_state, deck)
    game.game_state[STATE_CURRENT_STATE] = start
    game.game_state["topCard"] = deck.pop()
    game.game_state["deck"] = deck
    print("Starting Crazy 8s!\n")


def finish(game):
    print("Finished playing :)")


#==============================================================================
# helper methods
#==============================================================================

"""
player is the player object that *lost* the hand, since he is the only one that will have points added
"""
def score_hand(player):
    score = 0
    for c in player.hand:
        if c.val == 8:
            score = score + 50
        elif isinstance(c.val, str):
            score = score + 10
        else:
            score = score + c.val
    player.score = player.score + score

def deal(state, deck):
    state[STATE_PLAYERS][0].hand.extend(deck[0:8])
    sortCards(state[STATE_PLAYERS][0].hand)
    state[STATE_PLAYERS][1].hand.extend(deck[8:16])
    sortCards(state[STATE_PLAYERS][1].hand)
    deck = deck[16:52]


def sortCards(lst):
    lst.sort(key=lambda x: x.value, reverse=True)
    lst.sort(key=lambda x: x.suit, reverse=True)


def get_highest_score(players):
    score = -1
    for p in players:
        if p.score > score:
            score = p.score
    return score


#==============================================================================
# start the game
#==============================================================================
bartok = new Game(players, { "discard" : [] }, )
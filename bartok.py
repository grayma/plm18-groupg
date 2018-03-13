from starterpack import *
from random import shuffle

#==============================================================================
# Standard Deck
#==============================================================================

suits = ['hearts', 'diamonds', 'spades', 'clubs']
abbr_suits = ["h", "d", "s", "c"]
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


def get_deck():
    return [Card(value, suit) for value in values for suit in suits]


#==============================================================================
# board helpers
#==============================================================================

def game_status(player, state):
    print("\nTurn " + str(state[STATE_TURNS]))
    print("Showing %s info about the game." % (player.name))
    printBoard(state)
    print(player.hand)
    print()  # separator line
    
def printBoard(state):
    # see play() - topCard may be string or a card
    print("-----------------")
    print("|      %d %s      |" % (state['players'][0].score, state['players'][0].name[0]))
    print("|               |")
    print("|    top: %s    |" % state["topCard"].abbr())
    print("|               |")
    print("|      %s %d      |" % (state['players'][1].name[0], state['players'][1].score))
    print("-----------------")


#==============================================================================
# move functions
#==============================================================================

def play(player, state, input_dict):
    card = getCard(input_dict["card"])
    if not card:
        return "Invalid input."
    top_card = state["topCard"]
    discard = state["discard"]
    
    if not card in player.hand:
        return "Card not in hand."
    else:
        if card.value == "8":
            discard += [card, top_card] if not top_card.value == "x" else [card]
            player.hand.remove(card)
            valid = False
            while not valid:
                # choose a new suit
                new_suit = input("Choose a new suit (s, c, d, h): ")
                if new_suit in abbr_suits:
                    state["topCard"] = getCard("x" + new_suit)
                    valid = True
                else:
                    print("\nInvalid suit, try again.")
            return ""
        elif card.suit[0] == top_card.suit[0] or card.value[0] == top_card.value[0]:
            discard += [top_card] if not top_card.value == "x" else []
            state["topCard"] = card
            player.hand.remove(card)
            return ""
        else:
            return "Card does not match top card."

def draw(player, state, input):
    deck = state["deck"]
    
    if (not deck): #empty
        deck = shuffle(state["discard"])
        state["discard"] = []
        
    popped = deck.pop();
    print("\nYou drew: %s\n" % popped)
    player.hand += [popped]
    
    return ""

def placeholder(player, state, input):
    return ""

#==============================================================================
# moves
#==============================================================================

draw_move = Move("draw", draw, {})
play_move = Move("play", play, {"card": None})
placeholder_move = Move("placeholder", placeholder, {})


#==============================================================================
# transition functions
#==============================================================================

def transition_stub(state):
    pass
    
def reset_game(state):
    loser = [p for p in state["players"] if len(p.hand) > 0][0]
    winner = [p for p in state["players"] if len(p.hand) == 0][0]
    score_hand(winner, loser)
    deck = get_deck()
    shuffle(deck)
    shuffle(deck)
    shuffle(deck)
    for p in state["players"]:
        p.hand = []
    deal(state, deck)
    state["topCard"] = deck.pop()
    state["deck"] = deck
    state["discard"] = []
    
def conclude_game(state):
    score_hand(state)
    print("Final Score:")
    [print("%s: %d" % (p.name, p.score)) for p in state["players"]]


#==============================================================================
# transitions
#==============================================================================

# len(state[STATE_PLAYERS][0].hand) == 0 or len(state[STATE_PLAYERS][0].hand) == 0
main_to_main = Transition("main", (lambda state: not any(len(p.hand) == 0 for p in state["players"])), transition_stub)
main_to_main_reset = Transition("main",
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

states = [main, finish]


#==============================================================================
# players
#==============================================================================

players = []
for i in range(1, 3):
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
    game.game_state[STATE_CURRENT_STATE] = main
    game.game_state["topCard"] = deck.pop()
    game.game_state["deck"] = deck
    game.game_state["discard"] = []
    print("Starting Crazy 8s!\n")


def finish(game):
    print("Finished playing :)")


#==============================================================================
# helper methods
#==============================================================================

def score_hand(player_won, player_lost):
    score = 0
    for card in player_lost.hand:
        if card.value == "8":
            score = score + 50
        # all values are stored as strings, and all face cards are 10 points
        elif len(card.value) > 1:
            score = score + 10
        else:
            score = score + int(card.value)
    player_won.score = player_won.score + score

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
bartok = Game(players, { "startPlayer": 1 }, states, setup, finish)
bartok.start()
from starterpack import *
from random import shuffle

# Standard Deck
suits = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
deck = [Card(value, suit) for value in values for suit in suits]

# STATE_PLAYERS, STATE_CURRENT_STATE, STATE_DECK
STATE_TURN = "turns"
STATE_HEARTS = "hearts"
STATE_HEARTS_BROKEN = "broken"
STATE_PLAYED_CARDS = "played"
PLAYER_STATE_SCORE = "score"


# helper functions
def get_highest_score(players):
    score = -1
    for p in players:
        if p[PLAYER_STATE_SCORE] > score:
            score = p.state[PLAYER_STATE_SCORE]
    return score



# move functions
def pass3(player, state, input):
    num = player.number
    crds = ("card 1", "card 2", "card 3")
    #input should be already checked for validity before this point
    for i in range(3):
        str = input[crds[i]]
        if str[0] == "1":
            val = 10
        elif str[0] == "a":
            val = "ace"
        elif str[0] == "j":
            val = "jack"
        elif str[0] == "q":
            val = "queen"
        elif str[0] == "k":
            val = "king"
        else:
            val = str[0]

        n = 1
        if str[0] == "1":
            n = 2
        if str[n] == "c":
            suit = "clubs"
        elif str[n] == "d":
            suit = "diamonds"
        elif str[n] == "s":
            suit = "spades"
        elif str[n] == "h":
            suit = "hearts"

        c = Card(val, suit)
        index = -1
        for j in range(len(player.hand)):
            if player.hand[j] == c:
                index = j
        c = player.hand.pop(index)
        if num == 1:
            state['pass3s']['1'].append(c)
        elif num == 2:
            state['pass3s']['2'].append(c)
        elif num == 3:
            state['pass3s']['3'].append(c)
        elif num == 4:
            state['pass3s']['4'].append(c)
        c = None
    return ""
    #return "pass"


def play(player, state, input):
    return ""


def placeholder(player, state, input):
    return ""


# transition logic
def play(player, state, input):
    return ""


def placeholder(player, state, input):
    return ""


def transition_stub(game):
    pass


# move objects
pass3_move = Move("pass3", pass3, {"card 1": None, "card 2": None, "card 3": None})
play_move = Move("play", play, {"card": None})
placeholder_move = Move("placeholder", placeholder, {})

# transitions - happen by name
start_to_main = Transition("main", (lambda state: state[STATE_TURN] == 1), transition_stub)
main_to_broken = Transition("broken", (lambda state: state[STATE_HEARTS] == STATE_HEARTS_BROKEN), transition_stub)
broken_to_start = Transition("main", (lambda state: len(state[STATE_DECK]) == 0), transition_stub)
broken_to_finish = Transition("main", (lambda state: get_highest_score(state[STATE_PLAYERS]) >= 100), transition_stub)


def game_status(player, state):
    print("\nTurn " + str(state[STATE_TURN]))
    print("Showing %s info about the game." % (player.name))
    print(player.hand)
    print()  # separator line


# states
broken_transitions = [broken_to_start, broken_to_finish]
broken_moves = [play_move]
broken = State("broken", broken_transitions, broken_moves, game_status, False)

main_transitions = [main_to_broken]
main_moves = [play_move]
main = State("main", main_transitions, main_moves, game_status, False)

start_transitions = [start_to_main]
start_moves = [pass3_move]
start = State("start", start_transitions, start_moves, game_status, False)

finish = State("finish", None, [placeholder_move], game_status, True)

states = [start, main, broken, finish]

# players
players = []
for i in range(1, 5):
    name = input("What is the name of player " + str(i) + "? ")
    hand = []
    player = Player(name, {}, i, hand)
    players.append(player)


def deal(game, deck):
    players[0].hand.extend(deck[0:13])
    players[1].hand.extend(deck[13:26])
    players[2].hand.extend(deck[26:39])
    players[3].hand.extend(deck[39:52])


def setup(game):
    shuffle(deck)
    shuffle(deck)
    shuffle(deck)
    deal(game, deck)
    game.game_state[STATE_CURRENT_STATE] = start
    print("Starting Hearts!\n")


def finish(game):
    print("Finished playing :)")


hearts = Game(players, { "pass3s" : { "1" : [], "2" : [], "3" : [], "4" : [] }, "currentLead" : None }, states, setup, finish)
hearts.start()

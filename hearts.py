from starterpack import *
from random import shuffle
from collections import deque

# Standard Deck
suits = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


def get_deck():
    return [Card(value, suit) for value in values for suit in suits]


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
        if p.score > score:
            score = p.score
    return score


# move functions
def pass3(player, state, input):
    crds = ("card 1", "card 2", "card 3")
    # input should be already checked for validity before this point
    for i in range(3):
        str = input[crds[i]]
        c = getCard(str)
        index = -1
        for j in range(len(player.hand)):
            if player.hand[j] == c:
                index = j
        c = player.hand.pop(index)
        player.state["pass3s"].append(c)
        c = None
    return ""


def play(player, state, input):
    num = player.number
    str = input['card']
    c = getCard(str)
    if c.suit == "hearts":
        state[STATE_HEARTS] = STATE_HEARTS_BROKEN
    if state['played'][state['startPlayer']-1].isspace():
        state['currentLead'] = c.suit
    state['played'][num - 1] = str
    for j in range(len(player.hand)):
        if player.hand[j] == c:
            index = j
    c = player.hand.pop(index)
    return ""


def placeholder(player, state, input):
    return ""


# transition logic
def play_transition(state):
    num = -1
    val = -1
    cardVal = -1
    suit = state['currentLead']
    played_list = state['played']
    cardList = []
    for i in range(4):
        c = getCard(played_list[i])
        cardList.append(c)
        if c.value == 'ace':
            cardVal = 14
        elif c.value == 'jack':
            cardVal = 11
        elif c.value == 'queen':
            cardVal = 12
        elif c.value == 'king':
            cardVal = 13
        else:
            cardVal = int(c.value)
        if c.suit == suit and cardVal > val:
            val = cardVal
            num = i

    state['players'][num].state['accum'].extend(cardList)
    state["startPlayer"] = state['players'][num].number
    state["played"] = ["", "", "", ""]


def transition_stub(game):
    pass


"""
Logic to transition from main back to start
"""


def reset_game(state):
    score_hand(state)
    for p in state[STATE_PLAYERS]:
        p.hand = []
        p.state["accum"] = []
        p.state["pass3s"] = []
    deck = get_deck()
    shuffle(deck)
    shuffle(deck)
    shuffle(deck)
    deal(state, deck)
    state[STATE_HEARTS] = "unbroken"


"""
Logic to wrap up start step of game
"""


def pass_cards(state):
    for i in range(4):
        pass_hand = state[STATE_PLAYERS][(i + 1) % 4].hand
        cards_to_pass = state[STATE_PLAYERS][i].state["pass3s"]
        pass_hand += cards_to_pass
        sortCards(pass_hand)


def conclude_game(state):
    score_hand(state)
    print("Final Score:")
    [print("%s: %d" % (p.name, p.score)) for p in state["players"]]


# move objects
pass3_move = Move("pass3", pass3, {"card 1": None, "card 2": None, "card 3": None})
play_move = Move("play", play, {"card": None})
placeholder_move = Move("placeholder", placeholder, {})

# transitions - happen by name
start_to_main = Transition("main", (lambda state: state[STATE_TURN] == 1), pass_cards)
main_to_main = Transition("main", (lambda state: len(state[STATE_PLAYERS][0].hand) != 0), play_transition)
main_to_start = Transition("start", (
    lambda state: len(state[STATE_PLAYERS][0].hand) == 0 and get_highest_score(state[STATE_PLAYERS]) < 100), reset_game)
main_to_finish = Transition("finish", (lambda state: get_highest_score(state[STATE_PLAYERS]) >= 100), conclude_game)


def game_status(player, state):
    print("\nTurn " + str(state[STATE_TURN]))
    print("Showing %s info about the game." % (player.name))
    printBoard(state)
    print(player.hand)
    print()  # separator line


def printBoard(state):
    filler(state)
    print("-----------------")
    print("|      %d %s      |" % (state['players'][0].score, state['players'][0].name[0]))
   # n = state['players'][0].number
    print("|       %s     %d|" % (state['played'][0], state['players'][1].score))
    print("|%s %s       %s %s|" % (
    state['players'][3].name[0], state['played'][3], state['played'][1], state['players'][1].name[0]))
    print("|%d      %s      |" % (state['players'][3].score, state['played'][2]))
    print("|       %s %d     |" % (state['players'][2].name[0], state['players'][2].score))
    print("-----------------")


# Filler for grid to maintain formatting if a player hasnt played yet
def filler(state):
    #print(state["played"])
    for i in range(4):
        if (len(state['played'][i]) != 2 and len(state['played'][i]) != 3):
            state['played'][i] = "  "

    # % (state[0][0][0])


def score_hand(state):
    for i in range(4):
        s = 0
        lst = state['players'][i].state['accum']
        for j in range(len(lst)):
            if lst[j].suit == "hearts":
                s = s + 1
            if lst[j].suit == "spades" and lst[j].value == "queen":
                s = s + 13
        if s == 26:
            for t in range(4):
                state['players'][t].score = state['players'][t].score + 26
            state['players'][i].score = state['players'][i].score - 26
            return  # no need to check the rest of the players' scores
        else:
            state['players'][i].score = state['players'][i].score + s


# states
start_transitions = [start_to_main]
start_moves = [pass3_move]
start = State("start", start_transitions, start_moves, game_status, False)

main_transitions = [main_to_start, main_to_main, main_to_finish]
main_moves = [play_move]
main = State("main", main_transitions, main_moves, game_status, False)

finish = State("finish", None, [placeholder_move], game_status, True)

states = [start, main, finish]

# players
players = []
for i in range(1, 5):
    name = input("What is the name of player " + str(i) + "? ")
    hand = []
    player = Player(name, {"accum": [], "pass3s": []}, i, hand, 0)
    players.append(player)


def deal(state, deck):
    state[STATE_PLAYERS][0].hand.extend(deck[0:13])
    sortCards(state[STATE_PLAYERS][0].hand)
    state[STATE_PLAYERS][1].hand.extend(deck[13:26])
    sortCards(state[STATE_PLAYERS][1].hand)
    state[STATE_PLAYERS][2].hand.extend(deck[26:39])
    sortCards(state[STATE_PLAYERS][2].hand)
    state[STATE_PLAYERS][3].hand.extend(deck[39:52])
    sortCards(state[STATE_PLAYERS][3].hand)


def sortCards(lst):
    lst.sort(key=lambda x: x.value, reverse=True)
    lst.sort(key=lambda x: x.suit, reverse=True)


def setup(game):
    deck = get_deck()
    shuffle(deck)
    shuffle(deck)
    shuffle(deck)
    deal(game.game_state, deck)
    game.game_state[STATE_CURRENT_STATE] = start
    game.game_state[STATE_HEARTS] = "unbroken"
    print("Starting Hearts!\n")


def finish(game):
    print("Finished playing :)")


hearts = Game(players, {"currentLead": None, "played": ["", "", "", ""], "startPlayer": 1}, states, setup, finish)
hearts.start()

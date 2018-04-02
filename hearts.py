from starterpack import *
from random import shuffle

##
## ENVIRONMENT
##

suits = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
value_map = {'2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'jack' : 11, 'queen' : 12, 'king' : 13, 'ace' : 14}

GAME_HEARTS_BROKEN = 'is_hearts_broken'
GAME_PLAYED_CARDS = 'played_cards'
GAME_DECK = 'deck'

PLAYER_HAND = 'hand'
PLAYER_PLAYED = 'played'

def get_deck():
    return [Card(value, suit) for value in values for suit in suits]

def gamespace():
    return {
        GAME_HEARTS_BROKEN  : False,
        GAME_PLAYED_CARDS   : Pile([]),
        GAME_DECK           : Pile(get_deck())
    }

def playerspace():
    return {
        PLAYER_HAND         : Pile([]),
        PLAYER_PLAYED       : Card
    }

##
## HELPERS
##

def map_value(card):
    return values_map[card.value]

def lead(game):
    return game.gamespace[GAME_PLAYED_CARDS][0]

def last(game):
    return game.gamespace[GAME_PLAYED_CARDS][-1]

def score_pile(game, pile):
    s = 0
    for card in pile.cards:
        if card.suit == 'hearts':
            s += 1
        if card.suit == 'spades' and card.value == 'queen'
            s += 13
    return s

def score_turn(game):
    lead_suit = lead(game).suit
    p_card = p.playerspace[PLAYER_PLAYED]
    taking_it = None
    highest = -1
    for p in game.players:
        if p_card.suit == lead_suit and map_value(p_card) > highest:
            highest = map_value(p_card)
            taking_it = p
    score = score_pile(game.gamespace[GAME_PLAYED_CARDS])
    taking_it.score = score

def game_status(player, game):
    print("\nTurn " + str(game.turn))
    print("Showing %s info about the game." % (player.name))
    printBoard(game)
    print(player.playerspace[PLAYER_HAND])
    print()  # separator line

def printBoard(game):
    filler(game)
    players = game.players
    cards = game.gamespace[GAME_PLAYED_CARDS]
    print("-----------------")
    print("|      %d %s      |" % (players[0].score, players[0].name[0]))
    print("|       %s     %d|" % (cards[0], players[1].score))
    print("|%s %s       %s %s|" % (players[3].name[0], cards[3], cards[1], players[1].name[0]))
    print("|%d      %s      |" % (players[3].score, cards[2]))
    print("|       %s %d     |" % (players[2].name[0], players[2].score))
    print("-----------------")

# Filler for grid to maintain formatting if a player hasnt played yet
def filler(game):
    cards = game.gamespace[GAME_PLAYED_CARDS]
    for i in range(4):
        if (len(cards[i]) != 2 and len(cards[i]) != 3):
            cards[i] = "  "

def validate_pass3(game, player, subset):
    """
    Validates a subset actually being in a players hand or a valid play

    Checks existence in hand and suit
    """
    return "" if subset in player.playerspace[PLAYER_HAND].cards else "Cards must be in the passing players hand.":


def validate_play(game, player, card):
    """
    Returns "" if valid play, returns error message and why if not
    """
    if not card in player.playerspace[PLAYER_HAND].cards:
        return ""
    # first move of game and of turn, 2 of clubs required on 2nd turn (first turn after passing)
    if game.turn == 2: #first play turn
        if len(game.gamespace[GAME_PLAYED_CARDS]) == 0: #first player of the turn
            if (card.suit != 'clubs') and (card.value != '2'):
                return "First play must be 2 of clubs"
    # first move of turn, can't play hearts unless broken
    if (len(game.gamespace[GAME_PLAYED_CARDS]) == 0) and (not game.gamespace[GAME_HEARTS_BROKEN]) and (card.suit == 'hearts'):
        return "Can't play hearts unless hearts is broken"
    # if player has suit, they must match it. if they don't have suit, play anything and break hearts
    if len(game.gamespace[GAME_PLAYED_CARDS]) != 0:
        hand = player.playerspace[PLAYER_HAND]
        lead = game.gamespace[GAME_PLAYED_CARDS][0]
        for c in hand:
            if lead.suit == c.suit and c.suit != card.suit:
                return "If you can match the lead of the trick, you must do so."
    return ""


def getNextPlayer(player, game):
    i = (player.index + 1) % len(game.players)
    for p in game.players:
        if p.index == i:
            return p
    return None #shouldn't reach

def rotatePlayers(game):
    for p in game.players:
        p.index = (p.index + 1) % 4

def game_status(player, game):
    print("status")

##
## MOVES
##

def pass3(game, player, input):
    subset = None
    try:
        subset = [Card.from_abbr(value) for key, value in input.items()]
    except:
        return False
    if validate_pass3(game):
        player.playerspace[PLAYER_HAND].transfer_to(getNextPlayer(player, game).playerspace[PLAYER_HAND], subset)

def play(game, player, input):
    card = None
    try:
        card = Card.from_abbr(input["card"])
    except:
        return False
    if validate_play(game, player, card):
        if card.suit == 'hearts':
            game.gamespace[GAME_HEARTS_BROKEN] = True 
        player.playerspace[PLAYER_HAND].transfer_to(game.gamespace[GAME_PLAYED_CARDS], [card])
        player.playerspace[PLAYER_PLAYED] = card

Move("pass 3 cards", pass3, { "card 1" : None, "card 2" : None, "card 3" : None })
Move("play", play, { "card" : None })


start   = State("start"   , game_status   , [pass3]   , False )
main    = State("main"    , game_status   , [play]    , False )
finish  = State("finish"  , game_status   , []        , True  )

transitions = [
    Transition(start, main  , lambda game: game.turn == 2           , lambda game: x),
    Transition(main , main  , lambda game: not game_is_over(game)   , lambda game: x),
    Transition(main , finish, lambda game: game_is_over(game)       , lambda game: x),
]
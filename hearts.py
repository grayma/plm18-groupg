from starterpack import *
from random import shuffle

#################
## ENVIRONMENT ##
#################

GAME_HEARTS_BROKEN = 'is_hearts_broken'
GAME_PLAYED_CARDS = 'played_cards'
GAME_DECK = 'deck'

PLAYER_HAND = 'hand'
PLAYER_INTERMED = 'intermed'
PLAYER_PLAYED = 'played'

def get_deck():
    return Pile([Card(value, suit) for value in values for suit in suits])

def gamespace():
    return {
        GAME_HEARTS_BROKEN  : False,
        GAME_PLAYED_CARDS   : Pile([]),
        GAME_DECK           : Pile(get_deck())
    }

def playerspace():
    return {
        PLAYER_HAND         : Pile([]),
        PLAYER_INTERMED     : Pile([]),
        PLAYER_PLAYED       : None
    }

#############
## HELPERS ##
#############

def lead(game):
    return game.gamespace[GAME_PLAYED_CARDS][0]

def last(game):
    return game.gamespace[GAME_PLAYED_CARDS][-1]

def score_pile(game, pile):
    s = 0
    for card in pile.cards:
        if card.suit == 'hearts':
            s += 1
        if card.suit == 'spades' and card.value == 'queen':
            s += 13
    return s

def score_turn_and_clean(game):
    lead_suit = lead(game).suit
    taking_it = None
    highest = -1
    for p in game.players:
        p_card = p.playerspace[PLAYER_PLAYED]
        if p_card.suit == lead_suit and map_value(p_card) > highest:
            highest = map_value(p_card)
            taking_it = p
        #clean
        p.playerspace[PLAYER_PLAYED] = None
        game.gamespace[GAME_PLAYED_CARDS] = Pile([])

    score = score_pile(game.gamespace[GAME_PLAYED_CARDS])
    taking_it.score = score


def game_status(player, game):
    print("\nTurn " + str(game.turn))
    print("Showing %s info about the game." % (player.name))
    printBoard(game)
    print(player.playerspace[PLAYER_HAND])
    print()  # separator line

def printBoard(game):
    players = game.players
    cards = [p.playerspace[PLAYER_PLAYED] for p in players]
    cards = filler(cards)
    print("-----------------")
    print("|      %d %s      |" % (players[0].score, players[0].name[0]))
    print("|       %s     %d|" % (cards[0], players[1].score))
    print("|%s %s       %s %s|" % (players[3].name[0], cards[3], cards[1], players[1].name[0]))
    print("|%d      %s      |" % (players[3].score, cards[2]))
    print("|       %s %d     |" % (players[2].name[0], players[2].score))
    print("-----------------")

# Filler for grid to maintain formatting if a player hasnt played yet
def filler(cards):
    return ["  " if not card else card.value for card in cards]

def getNextPlayer(player, game):
    i = (player.index + 1) % len(game.players)
    for p in game.players:
        if p.index == i:
            return p
    return None #shouldn't reach

def rotatePlayers(game):
    for p in game.players:
        p.index = (p.index + 1) % 4

###########
## MOVES ##
###########

def validate_pass3(game, player, subset):
    """
    Validates a subset actually being in a players hand or a valid play

    Checks existence in hand and suit
    """
    for card in subset:
        if not card in player.playerspace[PLAYER_HAND].cards:
            return "Cards must be in the passing players hand."
    return ""


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

def finish_pass3(game):
    """
    Pass all the intermediate pass3 cards into the players hand after the turn is run.
    """
    for p in game.players:
        intermed = playerspace[PLAYER_INTERMED]
        intermed.transfer_to(p.playerspace[PLAYER_HAND], intermed.cards)

def f_pass3(game, player, input):
    subset = None
    try:
        subset = [Card.from_abbr(value) for key, value in input.items()]
    except:
        return False
    validation = validate_pass3(game, player, subset)
    if validation == "":
        player.playerspace[PLAYER_HAND].transfer_to(getNextPlayer(player, game).playerspace[PLAYER_INTERMED], subset)
    return validation

def f_play(game, player, input):
    card = None
    try:
        card = Card.from_abbr(input["card"])
    except:
        return False
    validation = validate_play(game, player, card)
    if validation == "":
        if card.suit == 'hearts':
            game.gamespace[GAME_HEARTS_BROKEN] = True 
        player.playerspace[PLAYER_HAND].transfer_to(game.gamespace[GAME_PLAYED_CARDS], [card])
        player.playerspace[PLAYER_PLAYED] = card
    return validation

pass3 = Move("pass3", f_pass3, { "card 1" : None, "card 2" : None, "card 3" : None })
play = Move("play", f_play, { "card" : None })


start   = State("start"   , game_status   , [pass3]   , False )
main    = State("main"    , game_status   , [play]    , False )
finish  = State("finish"  , game_status   , []        , True  )

transitions = [
    Transition(start, main  , finish_pass3(game)        , lambda game: game.turn == 2           ),
    Transition(main , main  , score_turn_and_clean(game), lambda game: not game_is_over(game)   ),
    Transition(main , finish, score_turn_and_clean(game), lambda game: game_is_over(game)       )
]

############################
## PRIMARY GAME FUNCTIONS ##
############################

def game_is_over(game):
    for p in game.players:
        if p.score >= 100:
            return p
    return None

def setup(game):
    deck = get_deck()
    shuffle(deck.cards)
    per_player = int(52 / len(game.players))
    for p in game.players:
        deck.transfer_to(p.playerspace[PLAYER_HAND], [deck.cards[i] for i in range(per_player)])

def finish(game):
    print()
    for p in game.players:
        print(p.score)

def get_players():
    ps = []
    for i in range(4):
        name = ""
        while name == "":
            name = input("What's the name of player @ index {} (can't be empty): ".format(i))
        p = Player(name, i)
        p.playerspace = playerspace()
        ps.append(p)
    return ps


def start_hearts():
    players = get_players()
    gs = gamespace()
    hearts = Game(players, 
                    gs, 
                    start, 
                    transitions, 
                    game_is_over, 
                    setup, 
                    finish, 
                    lambda prompt: input(prompt), 
                    lambda info: print(info))
    hearts.start()

if __name__ == '__main__':
    start_hearts()


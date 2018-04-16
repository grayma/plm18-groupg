from starterpack import *
from random import shuffle

WINNING_SCORE = 50

#==============================================================================
# player and game spaces
#==============================================================================

GAME_TOP_CARD = 'top_card'
GAME_PLAYED_CARDS = 'played_cards'
GAME_DISCARD  = 'discard'
GAME_DECK = 'deck'

def gamespace():
    return {
        GAME_TOP_CARD       : None,
        GAME_PLAYED_CARDS   : Pile([]),
        GAME_DISCARD        : Pile([]),
        GAME_DECK           : Pile([])
    }

def playerspace():
    return { }

#==============================================================================
# board helpers
#==============================================================================

def game_status(player, game):
    print("\nTurn " + str(game.turn))
    print("Showing %s info about the game." % (player.name))
    print_board(game)
    player.hand.sort()
    print(player.hand, "\n")
    
def print_board(game):
    # see play() - topCard may be string or a card
    players = game.players
    print("-----------------")
    print("|      %d %s      |" % (players[0].score, game.players[0].name[0]))
    print("|               |")
    print("|    top: %s    |" % game.gamespace[GAME_TOP_CARD].abbr())
    print("|               |")
    print("|      %s %d      |" % (players[1].name[0], players[1].score))
    print("-----------------")

#==============================================================================
# move validation functions
#==============================================================================

def validate_play(game, player, card):
    top_card = game.gamespace[GAME_TOP_CARD]
    #Check that it's in the players hand
    if not card in player.hand:
        return "Card not in hand."
    #Check that the suit or value matches, or it's an 8
    if not card.suit == top_card.suit and not card.value == top_card.value and not card.value == '8':
        return "Card must match the suit or value of the top card, or be an 8 of any suit."
    return "";

#==============================================================================
# can_move functions
#==============================================================================

def f_can_play(game, player):
    top_card = game.gamespace[GAME_TOP_CARD]
    for c in player.hand:
        if c.suit == top_card.suit or c.value == top_card.value or c.value == '8':
            return True
    return False

def f_can_draw(game, player):
    deck = game.gamespace[GAME_DECK]
    discard = game.gamespace[GAME_DISCARD]
    if not deck: #empty so transfer discard to deck
        discard.transfer_to(deck, discard.cards)
        deck.shuffle()
    return deck #if deck still empty, can't draw

#==============================================================================
# move functions
#==============================================================================

def f_play(game, player, input_dict):
    card = None
    try:
        card = Card.from_abbr(input_dict["card"])
    except:
        return "Invalid card entered."
    validate = validate_play(game, player, card)
    if validate == "":
        discard = game.gamespace[GAME_DISCARD]
        top_card = game.gamespace[GAME_TOP_CARD]
        if not top_card.value == "x":
            discard.cards = discard.cards + [top_card]
        if card.value == "8":
            player.hand.transfer_to(discard, [card])
            new_suit = get_suit()
            # top card will only have a suit, so create a stubbed card with no value
            top_card = Card("x", suit_abbr_map[new_suit])
        else:
            player.hand.remove(card)
            top_card = card
        game.gamespace[GAME_TOP_CARD] = top_card
    return validate

def f_draw(game, player, input_dict):
    deck = game.gamespace[GAME_DECK]
    discard = game.gamespace[GAME_DISCARD]
    popped = deck.pop();
    print("\nYou drew: %s\n" % popped)
    player.hand.cards = player.hand.cards + [popped]
    return ""

#==============================================================================
# state logic functions
#==============================================================================

def end_turn(game):
    if round_is_over(game):
        print("\nRound is over! Scoring game...")
        winner = [p for p in game.players if p.hand.is_empty()][0]
        loser  = [p for p in game.players if not p.hand.is_empty()][0]
        winner.score = winner.score + score_hand(loser)
        if not game_is_over(game):
            print("Resetting board...")
            for p in game.players:
                p.hand = Pile([])
            game.setup(game)

#==============================================================================
# exit conditions
#==============================================================================
    
def round_is_over(game):
    """
    Returns true if a player's hand is empty, aka the round is over
    """
    # round is over if we find a player whose hand is empty
    for p in game.players:
        if p.hand.is_empty():
            return True
    return False

def game_is_over(game):
    """
    Returns true if a player's score is over 50
    """
    for p in game.players:
        if p.score >= 50:
            return True
    return False

#==============================================================================
# states and transitions
#==============================================================================

draw = Move("draw", f_can_draw  , f_draw , { }              )
play = Move("play", f_can_play  , f_play , { "card" : None })

main    = State("main"    , game_status   , [draw, play], end_turn    , False, round_is_over)
finish  = State("finish"  , game_status   , []          , None        , True , None         )

transitions = [
    Transition(main , main  , lambda game: not game_is_over(game)                          ),
    Transition(main , finish, lambda game: game_is_over(game)                              )
]

#==============================================================================
# players
#==============================================================================

def get_players():
    ps = []
    for i in range(2):
        name = ""
        while name == "":
            name = input("What's the name of player @ index {} (can't be empty): ".format(i))
        p = Player(name, i)
        p.playerspace = playerspace()
        ps.append(p)
    return ps 


#==============================================================================
# beginning/end game functions
#==============================================================================

def setup(game):
    deck = Deck()
    deck.shuffle()
    deck.deal(game.players, 8)
    game.gamespace[GAME_TOP_CARD] = deck.pop()
    game.gamespace[GAME_DECK] = deck
    game.gamespace[GAME_DISCARD] = Pile([])
    
def finish(game):
    print("Final Score:")
    [print("%s: %d" % (p.name, p.score)) for p in game.players]

#==============================================================================
# helper methods
#==============================================================================

def get_suit():
    new_suit = input("Choose a new suit (s, c, d, h): ")
    while not new_suit in suit_abbr_map.keys():
        # choose a new suit
        print("\nInvalid suit, try again.")
        new_suit = input("Choose a new suit (s, c, d, h): ")
    return new_suit

def score_hand(player):
    score = 0
    for card in player.hand:
        if card.value == "8":
            score = score + 50
        # all values are stored as strings, and all face cards are 10 points
        elif len(card.value) > 1:
            score = score + 10
        else:
            score = score + int(card.value)
    return score

#==============================================================================
# start the game
#==============================================================================
def start_bartok():
    players = get_players()
    gs = gamespace()
    bartok = Game(players = players, 
                    gamespace = gs, 
                    start_state = main, 
                    transitions = transitions,
                    setup = setup, 
                    finish = finish, 
                    get = lambda prompt: input(prompt), 
                    post = lambda info: print(info))
    bartok.start()

if __name__ == '__main__':
    start_bartok()
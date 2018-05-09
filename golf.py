from gaming import *

# ==============================================================================
# player and game spaces
# ==============================================================================

DECK_TOP_CARD = 'top_card'
GAME_DISCARD = 'discard'
GAME_DECK = 'deck'
DISC_TOP_CARD = 'disc_top'
P_REVEALED = 'revealed'
P_ALL_REVEALED = 'all_revealed'
ROUND_IS_OVER = 'round_is_over'


def gamespace():
    return {
        DECK_TOP_CARD: None,
        GAME_DISCARD: Pile([]),
        GAME_DECK: Pile([]),
        DISC_TOP_CARD: None,
        ROUND_IS_OVER: False
    }


def playerspace():
    
    pdict = {
        P_REVEALED: [False, False, False, False, False, False]
    }
    pdict[P_ALL_REVEALED] = lambda p: all_revealed(p)
    return pdict


def all_revealed(p):
        for i in p.playerspace[P_REVEALED]:
            if(not i):
                return False
        return True

# ==============================================================================
# board helpers
# ==============================================================================

def game_status(player, game):
    print("\nTurn " + str(game.turn))
    print("Showing %s info about the game." % (player.name))
    print_board(game)


def print_board(game):
    if len(game.players) == 4:
        players = game.players
        print("------------------------")
        print("|    %s %d  _____        |" % (game.players[0].name[0], players[0].score))
        print("|        |%s|%s|%s|       |" % (
        get_sym(game.players[0], 0), get_sym(game.players[0], 1), get_sym(game.players[0], 2)))
        print("|        |%s|%s|%s|    %s %d|" % (
        get_sym(game.players[0], 3), get_sym(game.players[0], 4), get_sym(game.players[0], 5), game.players[1].name[0],
        players[1].score))
        print("|  ___            ___  |")
        print("| |%s|%s|          |%s|%s| |" % (
        get_sym(game.players[3], 0), get_sym(game.players[3], 1), get_sym(game.players[1], 0),
        get_sym(game.players[1], 1)))
        print("| |%s|%s|  |X||%s|  |%s|%s| |" % (
        get_sym(game.players[3], 2), get_sym(game.players[3], 3), abbr(game.gamespace[DISC_TOP_CARD]),
        get_sym(game.players[1], 2), get_sym(game.players[1], 3)))
        print("| |%s|%s|          |%s|%s| |" % (
        get_sym(game.players[3], 4), get_sym(game.players[3], 5), get_sym(game.players[1], 4),
        get_sym(game.players[1], 5)))
        print("|%s %d      _____        |" % (game.players[3].name[0], players[3].score))
        print("|        |%s|%s|%s|       |" % (
        get_sym(game.players[2], 0), get_sym(game.players[2], 1), get_sym(game.players[2], 2)))
        print("|        |%s|%s|%s| %s %d   |" % (
        get_sym(game.players[2], 3), get_sym(game.players[2], 4), get_sym(game.players[2], 5), game.players[2].name[0],
        players[2].score))
        print("|                       |")
        print("------------------------")
    if len(game.players) == 2:
        players = game.players
        print("------------------------")
        print("|    %s %d  _____        |" % (game.players[0].name[0], players[0].score))
        print("|        |%s|%s|%s|       |" % (
            get_sym(game.players[0], 0), get_sym(game.players[0], 1), get_sym(game.players[0], 2)))
        print("|        |%s|%s|%s|       |" % (
            get_sym(game.players[0], 3), get_sym(game.players[0], 4), get_sym(game.players[0], 5)))
        print("|                      |" )
        print("|        |X||%s|        |" % (abbr(game.gamespace[DISC_TOP_CARD])))
        print("|                      |")
        print("|        |%s|%s|%s|       |" % (
            get_sym(game.players[1], 0), get_sym(game.players[1], 1), get_sym(game.players[1], 2)))
        print("|        |%s|%s|%s| %s %d   |" % (
            get_sym(game.players[1], 3), get_sym(game.players[1], 4), get_sym(game.players[1], 5),
            game.players[1].name[0],
            players[1].score))
        print("|                      |")
        print("------------------------")
    else:
        return ""

def abbr(card):
    if card.value == "10":
        return 10
    else:
        return card.abbr()[0]

def get_sym(player, n):
    if(player.playerspace[P_REVEALED][n]):
        return get_short(player.hand[n])
    return "-"

def get_short(card):
    if(card.value == "queen"):
        return "q"
    if(card.value == "king"):
        return "k"
    if(card.value == "jack"):
        return "j"
    if(card.value == "ace"):
        return "a"
    else:
        return card.value

# ==============================================================================
# can_move functions
# ==============================================================================

"""
    There are two mains states of play, start and main. Since each state has
    a single possible move, there is no need for can_move validation -- if the
    player has no valid moves in a given state, the round or game is over
"""

# ==============================================================================
# move functions
# ==============================================================================

def reveal(player, n):
    player.playerspace[P_REVEALED][int(n) - 1] = True

def f_draw(game, player, input_dict):
    #give option to draw from deck OR discard
    #give player card value
    #allow user to choose which slot to put the card in
    #if choice is already revealed, do nothing
    #if choice is not revealed, reveal it and replace card
    card = None
    resp = input("Would you like to pick from the deck or discard pile? ").format()
    if resp == "deck":
        card = game.gamespace[DECK_TOP_CARD]
        game.gamespace[DECK_TOP_CARD] = game.gamespace[GAME_DECK].pop()
    elif resp == "discard":
        card = game.gamespace[DISC_TOP_CARD]
    else:
        return "Invalid pile chosen."
    print("You picked a %s" % (card.value))
    
    resp = input("Where would you like to place your card (1 to 6 or discard?): ").format()
    if resp in list("123456"):
        game.gamespace[DISC_TOP_CARD] = player.hand[int(resp) - 1]
        player.hand.cards[int(resp) - 1] = card
        reveal(player, resp)
    elif resp == "discard":
        game.gamespace[DISC_TOP_CARD] = card
    return ""

def f_flip(game, player, input_dict):
    c1 = input_dict["card 1 (1 to 6)"]
    c2 = input_dict["card 2 (1 to 6)"]
    reveal(player, c1)
    reveal(player, c2)
    print_board(game)
    f_draw(game, player, {})
    return ""

# ==============================================================================
# state logic functions
# ==============================================================================

def end_turn(game):
    print("Ending turn...")
    if round_is_over(game):
        game.gamespace[ROUND_IS_OVER] = True
        score(game)
        if not game_is_over(game):
            print("Resetting board...")
            for p in game.players:
                p.playerspace[P_REVEALED] = [False, False, False, False, False, False]
                p.hand = Pile([])
            game.setup(game)
    else:
        game.gamespace[ROUND_IS_OVER] = False

def score(game):
    for p in game.players:
        if(p.hand.cards[0].value != p.hand.cards[3].value):
            p.score = p.score + golf_val(p.hand.cards[0])
            p.score = p.score + golf_val(p.hand.cards[3])
        if (p.hand.cards[1].value != p.hand.cards[4].value):
            p.score = p.score + golf_val(p.hand.cards[1])
            p.score = p.score + golf_val(p.hand.cards[4])
        if (p.hand.cards[2].value != p.hand.cards[5].value):
            p.score = p.score + golf_val(p.hand.cards[2])
            p.score = p.score + golf_val(p.hand.cards[5])

def golf_val(card):
    if card.val() == 14:
        return 1
    if card.val() == 2:
        return -2
    if card.val() == 13:
        return 0
    if card.val() >= 10:
        return 10
    else:
        return card.val()

# ==============================================================================
# exit conditions
# ==============================================================================

def round_is_over(game):
    """
    Returns true if a player's cards have all been revealed
    """
    # round is over if we find a player whose hand is empty
    for p in game.players:
        if p.playerspace[P_ALL_REVEALED](p):
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


# ==============================================================================
# states and transitions
# ==============================================================================
#"discard or deck?": None
draw = Move("draw", lambda game, player: True, f_draw, {})
flip = Move("flip", lambda game, player: True, f_flip, {"card 1 (1 to 6)": None, "card 2 (1 to 6)": None})

start  = State("start" , game_status, [flip], end_turn, False, round_is_over)
main   = State("main"  , game_status, [draw], end_turn, False, round_is_over)
finish = State("finish", game_status, []    , None    , True , None         )

transitions = [
    Transition(start, main  , lambda game: True                             ),
    Transition(main , main  , lambda game: not game.gamespace[ROUND_IS_OVER]),
    Transition(main , start , lambda game: not game_is_over(game)           ),
    Transition(main , finish, lambda game: game_is_over(game)               )
]


# ==============================================================================
# beginning/end game functions
# ==============================================================================

def setup(game):
    deck = Deck()
    deck.shuffle()
    deck.deal(game.players, 6)
    game.gamespace[DECK_TOP_CARD] = deck.pop()
    game.gamespace[GAME_DECK] = deck
    game.gamespace[DISC_TOP_CARD] = deck.pop()
    game.gamespace[GAME_DISCARD] = Pile([])

def finish(game):
    print("Final Score:")
    [print("%s: %d" % (p.name, p.score)) for p in game.players]


# ==============================================================================
# start the game
# ==============================================================================
def start_golf():
    resp = input("How many players (2 or 4)? ").format()
    players = get_players(int(resp), playerspace)
    gs = gamespace()
    golf = Game(players=players,
                  gamespace=gs,
                  start_state=start,
                  transitions=transitions,
                  setup=setup,
                  finish=finish,
                  get=lambda prompt: input(prompt),
                  post=lambda info: print(info))
    golf.start()


if __name__ == '__main__':
    start_golf()

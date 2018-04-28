from gaming import *

# ==============================================================================
# player and game spaces
# ==============================================================================

DECK_TOP_CARD = 'top_card'
GAME_DISCARD = 'discard'
GAME_DECK = 'deck'
DISC_TOP_CARD = 'disc_top'


def gamespace():
    return {
        DECK_TOP_CARD: None,
        GAME_DISCARD: Pile([]),
        GAME_DECK: Pile([]),
        DISC_TOP_CARD: None
    }


def playerspace():
    return {}


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
    if(player.revealed[n]):
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
# move validation functions
# ==============================================================================

def validate_play(game, player, card):
    top_card = game.gamespace[GAME_TOP_CARD]
    # Check that it's in the players hand
    if not card in player.hand:
        return "Card not in hand."
    return "";


# ==============================================================================
# can_move functions
# ==============================================================================

def f_can_flip(game, player):
    if(game.turn == 1):
        return True
    return False

def f_can_draw(game, player):
    deck = game.gamespace[GAME_DECK]
    return deck  # if deck still empty, can't draw


# ==============================================================================
# move functions
# ==============================================================================

def f_draw(game, player, input_dict):
    #give option to draw from deck OR discard
    #give player card value
    #allow user to choose which slot to put the card in
    #if choice is already revealed, do nothing
    #if choice is not revealed, reveal it and replace card
    card = None
    resp = input("Would you like to pick from the deck or discard? ").format()
    if(resp == "deck"):
        card = game.gamespace[DECK_TOP_CARD]
        game.gamespace[DECK_TOP_CARD] = game.gamespace[GAME_DECK].pop()
    elif(resp == "discard"):
        card = game.gamespace[DISC_TOP_CARD]
    print("You picked a %s" % (card.value))

    #print("Where would you like to place your card (1 to 6 or discard?")
    resp = input("Where would you like to place your card (1 to 6 or discard?) ").format()
    if(resp == "1"):
        game.gamespace[DISC_TOP_CARD] = player.hand[int(resp) - 1]
        player.hand.cards[int(resp) - 1] = card
        reveal(player, resp)
    if (resp == "2"):
        game.gamespace[DISC_TOP_CARD] = player.hand[int(resp) - 1]
        player.hand.cards[int(resp) - 1] = card
        reveal(player, resp)
    if (resp == "3"):
        game.gamespace[DISC_TOP_CARD] = player.hand[int(resp) - 1]
        player.hand.cards[int(resp) - 1] = card
        reveal(player, resp)
    if (resp == "4"):
        game.gamespace[DISC_TOP_CARD] = player.hand[int(resp) - 1]
        player.hand.cards[int(resp) - 1] = card
        reveal(player, resp)
    if (resp == "5"):
        game.gamespace[DISC_TOP_CARD] = player.hand[int(resp) - 1]
        player.hand.cards[int(resp) - 1] = card
        reveal(player, resp)
    if (resp == "6"):
        game.gamespace[DISC_TOP_CARD] = player.hand[int(resp) - 1]
        player.hand.cards[int(resp) - 1] = card
        reveal(player, resp)
    if (resp == "discard"):
        game.gamespace[DISC_TOP_CARD] = card
    return ""

def reveal(player, n):
    player.revealed[int(n) - 1] = True



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
    if round_is_over(game):
        score(game)
        if not game_is_over(game):
            print("Resetting board...")
            for p in game.players:
                p.revealed = [False, False, False, False, False, False]
                p.hand = Pile([])
            game.setup(game)
            game.state = start

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
    Returns true if a player's hand is empty, aka the round is over
    """
    # round is over if we find a player whose hand is empty
    for p in game.players:
        if p.all_revealed():
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
draw = Move("draw", f_can_draw, f_draw, {})
flip = Move("flip", f_can_flip, f_flip, {"card 1 (1 to 6)": None, "card 2 (1 to 6)": None})

start = State("start", game_status, [flip], end_turn, False, round_is_over)
main = State("main", game_status, [draw], end_turn, False, round_is_over)
finish = State("finish", game_status, [], None, True, None)

transitions = [
    Transition(start, main, lambda game: not game_is_over(game)),
    Transition(main, main, lambda game: not game_is_over(game)),
    Transition(main, finish, lambda game: game_is_over(game))
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
    game.state = start

def finish(game):
    print("Final Score:")
    [print("%s: %d" % (p.name, p.score)) for p in game.players]


# ==============================================================================
# helper methods
# ==============================================================================


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

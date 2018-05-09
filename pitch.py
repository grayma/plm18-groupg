from gaming import *
from collections import deque

#################
## ENVIRONMENT ##
#################

GAME_BID = 'bid'
GAME_TRUMP = 'trump'
GAME_HIGH = 'high'
GAME_LOW = 'low'
GAME_GAME = 'game_'
GAME_BIDDER = 'bidder'
GAME_PLAYED_CARDS = 'played_cards'
GAME_RESET = 'reset'
GAME_DEALER = 'dealer'

PLAYER_PLAYED = 'played'
STACK = 'stack'

TURNS_PER_ROUND = 14


def gamespace():
    return {
        GAME_HIGH: 0,
        GAME_LOW: 20,
        GAME_BID: 0,
        GAME_TRUMP: " ",
        GAME_GAME: [0, 0, 0, 0],
        GAME_PLAYED_CARDS: Pile([]),
        GAME_BIDDER: "",
        GAME_RESET: False,
        GAME_DEALER: None
    }


def playerspace():
    return {
        STACK: Pile([]),
        PLAYER_PLAYED: None
    }


#############
## HELPERS ##
#############

def lead(game):
    return game.gamespace[GAME_PLAYED_CARDS][0]

def last(game):
    return game.gamespace[GAME_PLAYED_CARDS][-1]

def select_dealer(game):
    players = game.players
    game.gamespace[GAME_DEALER] = players[0] if not game.gamespace[GAME_DEALER] else getNextPlayer(game.gamespace[GAME_DEALER], game)
    i = players.index(game.gamespace[GAME_DEALER])
    #Rotate based on the actual index in the list, not player.index
    rotatePlayers(players, 3 - i)

def score_pile(game):
    game_Score = 0
    tie = False
    g_p = None
    scores = [0,0,0,0]
    n = 0
    for p in game.players:
        s = 0
        g = 0
        pile = p.playerspace[STACK]
        for card in pile:
            #Currently does not work at all for some reason....
            #ex. player was supposed to get 4 points but 3 players got 1 pt each

            # suit is the suit 'Spades' but trump is only the letter 's'???
            # however this checks each card against the jack, high and low of trump that has been kept track of else where
            if card.suit == game.gamespace[GAME_TRUMP] and card.value == 'jack':
                s += 1
            if card.suit == game.gamespace[GAME_TRUMP] and card.val() == game.gamespace[GAME_HIGH]:
                s += 1
            if card.suit == game.gamespace[GAME_TRUMP] and card.val() == game.gamespace[GAME_LOW]:
                s += 1
            #this code calculates the game
            if card.val() == 10:
                g += 10
            if card.val() == 11:
                g += 1
            if card.val() == 12:
                g += 2
            if card.val() == 13:
                g += 3
            if card.val() == 14:
                g += 4
        #if there is a tie in the game, then no one should get the point for game
        if g == game_Score and g > 0:
            tie = True
        #If the score calculated is greater than the previous player, then get the player that should earn the point
        if g > game_Score:
            game_Score = g
            tie = False
            g_p = n
        #Add the score earned so far to the score array
        scores[n] += s
        n += 1

    #after all game points have been added together, add a point for game to the index of the player who should have earned it
    scores[g_p] += 1
    #Now that all points for the round have been put together, we can give the points to the players.
    for p in game.players:
        i = 0
        #If the player was the bidder and does not get their bid, they get the negative of their bid added to their score
        if p.name == game.gamespace[GAME_BIDDER].name and scores[i] < game.gamespace[GAME_BID]:
            p.score -= game.gamespace[GAME_BID]
        else:
            p.score += scores[i]
        i += 1

def game_status(player, game):
    print("Showing %s info about the game." % (player.name))
    printBoard(game)
    player.hand.sort()
    print(player.hand)
    print()  # separator line


def printBoard(game):
    # Sort the players based on index, since we are rotating the actual list of players
    players = sorted(game.players, key=lambda p: p.index)
    cards = filler([p.playerspace[PLAYER_PLAYED] for p in players])
    print("------------------")
    print("|t:%s     %d %s   b:%d|" % (game.gamespace[GAME_TRUMP][0], players[0].score, players[0].name[0], game.gamespace[GAME_BID]))
    print("|        %s     %d|" % (cards[0], players[1].score))
    print("|%s %s       %s %s|" % (players[3].name[0], cards[3], cards[1], players[1].name[0]))
    print("|%d       %s      |" % (players[3].score, cards[2]))
    print("|       %s %d       |" % (players[2].name[0], players[2].score))
    print("------------------")


# Filler for grid to maintain formatting if a player hasnt played yet
def filler(cards):
    return ["   " if not card else card.abbr() + " " for card in cards]

def getNextPlayer(player, game):
    i = (player.index + 1) % len(game.players)
    for p in game.players:
        if p.index == i:
            return p
    return None  # shouldn't reach


def rotatePlayers(game, r_param):
    """ r_param is the number of rotations to perform on the list """
    dq = deque(game.players)
    dq.rotate(r_param)
    game.players = list(dq)


###########
## MOVES ##
###########

def validate_play(game, player, card):
    """
    Returns "" if valid play, returns error message and why if not
    """
    if not card in player.hand.cards:
        return "Cards must be in the passing players hand."
    # if player has suit, they must match it. if they don't have suit, play anything and break hearts
    if len(game.gamespace[GAME_PLAYED_CARDS]) != 0:
        hand = player.hand
        lead = game.gamespace[GAME_PLAYED_CARDS][0]
        for c in hand:
            if lead.suit == c.suit and c.suit != card.suit:
                return "If you can match the lead of the trick, you must do so."
    return ""

def pick_trump(game):
    game_status(game.gamespace[GAME_BIDDER], game)
    resp = input("%s, please select a trump suit ('clubs', 'diamonds', 'spades', or 'hearts') " % game.gamespace[GAME_BIDDER].name).format()
    if resp[0] == 'c' or resp[0] == 'd' or resp[0] == 's' or resp[0] == 'h':
        game.gamespace[GAME_TRUMP] = resp
    rotatePlayers(game, 4 - game.gamespace[GAME_BIDDER].index)


def score_turn_and_clean(game):
    """
    Score turn and clean is to be called when the current round ends
    (Each player has played one card)
    """
    lead_suit = lead(game).suit
    taking_it = None
    highest = -1
    for p in game.players:
        p_card = p.playerspace[PLAYER_PLAYED]
        #if trump is played, all other cards should be compared to it.
        if p_card.suit == game.gamespace[GAME_TRUMP] and lead_suit != game.gamespace[GAME_TRUMP]:
            lead_suit = p_card.suit
            highest = -1
        if p_card.suit == lead_suit and map_value(p_card) > highest:
            highest = map_value(p_card)
            taking_it = p
        # clean playerspace
        p.playerspace[PLAYER_PLAYED] = None

    rotatePlayers(game, 4 - game.players.index(taking_it))
    taking_it.playerspace[STACK].cards.extend(game.gamespace[GAME_PLAYED_CARDS])
    # clean gamespace
    game.gamespace[GAME_PLAYED_CARDS] = Pile([])

    if (round_is_over(game)):
        score_pile(game)
        # Have to run our setup function again at the start of each round
        #game.setup(game)


def f_bid(game, player, input):
    n = None
    if input['bid'] == "pass":
        return ""
    try:
        n = int(input['bid'])
    except:
        return "Must be a number from 0 to 4 or 'pass'"
    if n == game.gamespace[GAME_BID] and game.gamespace[GAME_DEALER].index == player.index:
        game.gamespace[GAME_BID] = n
        game.gamespace[GAME_BIDDER] = player
        return ""
    if n <= game.gamespace[GAME_BID]:
        return ""
    if n > 4 or n < 2:
        return "Invalid bid"
    game.gamespace[GAME_BID] = n
    game.gamespace[GAME_BIDDER] = player
    return ""

def f_play(game, player, input):
    card = None
    try:
        card = Card.from_abbr(input["card"])
    except:
        return "Invalid card input."
    validation = validate_play(game, player, card)
    if validation == "":
        player.hand.transfer_to(game.gamespace[GAME_PLAYED_CARDS], [card])
        player.playerspace[PLAYER_PLAYED] = card
        if card.suit == game.gamespace[GAME_TRUMP] and card.val() > game.gamespace[GAME_HIGH]:
            game.gamespace[GAME_HIGH] = card.val()
        if card.suit == game.gamespace[GAME_TRUMP] and card.val() < game.gamespace[GAME_LOW]:
            game.gamespace[GAME_LOW] = card.val()
    return validation

bid = Move("bid", lambda game, player: True, f_bid, {"bid": None})
play = Move("play", lambda game, player: True, f_play, {"card": None})

start = State("start", game_status, [bid], pick_trump, False)
main = State("main", game_status, [play], score_turn_and_clean, False)
finish = State("finish", game_status, [], score_turn_and_clean, True)

transitions = [
    Transition(start, main, lambda game: True),  # always transition from start to main
    Transition(main, start, lambda game: round_is_over(game)),  # transition if the round is over but game is not
    Transition(main, main, lambda game: not game_is_over(game)),
    Transition(main, finish, lambda game: game_is_over(game))
]


############################
## PRIMARY GAME FUNCTIONS ##
############################

def round_is_over(game):
    for p in game.players:
        if p.hand.is_empty() and not game.gamespace[GAME_RESET]:
            game.gamespace[GAME_RESET] = True
            return True
        if game.gamespace[GAME_RESET]:
            game.setup(game)
            game.gamespace[GAME_RESET] = False
            return True
    return False


def game_is_over(game):
    for p in game.players:
        if p.score >= 15:
            return p
    return None


def setup(game):
    deck = Deck()
    deck.shuffle()
    deck.deal(game.players, 6)
    game.gamespace[GAME_BID] = 0
    select_dealer(game)


def finish(game):
    print()
    for p in game.players:
        print(p.name, str(p.score))


def start_pitch():
    players = get_players(4, playerspace)
    gs = gamespace()
    pitch = Game(players=players,
                  gamespace=gs,
                  start_state=start,
                  transitions=transitions,
                  setup=setup,
                  finish=finish,
                  get=lambda prompt: input(prompt),
                  post=lambda info: print(info))
    pitch.start()


if __name__ == '__main__':
    start_pitch()

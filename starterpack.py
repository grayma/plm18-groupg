import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Game
#  Start
#    Choose player to go - game.start() #inits game loop
#    Game initiates turn - loop of running all players moves, validating, updating state (public and player)
#      Player move - player[n].play()
#        Player requests game state (public state, private not available) - game.getVisibleState()
#        Player makes move and return
#          - logic in player[n].play()
#        Game validates Player move - game.validate(move) if not valid, remake move
#          Boolean conditions on public and private state
#        Next player move go back to Player Move with next player

# Hearts State
# Main Deck main_deck [ card ]
# Game Played Cards played_cards int
# Hearts Broken? hearts_broken true/false
#
# Player Deck [ card ]
# Player Cards Taken [ card ]
# Player Score [ card ]

"""
Game state dict constants
"""
STATE_PLAYERS = "players"
STATE_CURRENT_STATE = "state"
STATE_DECK = "deck"
STATE_TURNS = "turns"

"""
Wrapper for a Player playing the game
"""

class Player:
    def __init__(self, name, state, number, hand, score):
        self.name = name
        self.state = state
        self.number = number
        self.hand = hand
        self.score = 0


"""
Wrapper for a playing card
"""

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return str(self.value) + ' ' + self.suit
    def __eq__(self, other):
        if(str(self.suit) == str(other.suit) and str(self.value) == str(other.value)):
            return True
        else:
            return False



"""
Wrapper containing new and old game state and new and old player state to represent the
difference before and after a potential player's move.
`name` is the name of the move
`f` is the function that actually executes the move, taking in game_state and 
    required_input. Includes interaction with player. Returns "" if move successful, 
    an error message if needs to go again (rule break)
`required_args` dictionary representing required input for the move, game asks for key
"""


class Move:
    def __init__(self, name, f, required_input):
        self.name = name
        self.f = f
        self.required_input = required_input


"""
Class representing a game's state machine
`name` name of the state the game is in
`transitions` list of Transition's available in this state
`available_moves` list of available moves
`game_status` function taking a player and game_state showing player what info they need
`final_state` bool indicating whether or not game has finished
"""


class State:
    def __init__(self, name, transitions, available_moves, game_status, final_state):
        self.name = name
        self.transitions = transitions
        self.available_moves = {m.name: m for m in available_moves}
        self.game_status = game_status
        self.final_state = final_state

    def move(self, player, game_state):
        """Makes a move for a player given the current game state."""

        # figure out which move to use
        print("It is now %s's move, please pass the computer and press enter when %s has the computer." % (
            player.name, player.name))
        input()

        self.game_status(player, game_state)
        print("Available moves (type move name to use):")
        for mname in self.available_moves.keys():
            print(mname)
        selected = ""
        while selected not in self.available_moves.keys():
            selected = input("Please choose a valid move to execute: ")
        selected = self.available_moves[selected]

        # make move
        moved = False
        while not moved:
            print(
                "For this move we need the following (if card, use the format: 'vs' without quotes where v is the "
                "value of the card\n(number if non-face/ace card or a, k, q, j for ace, king, queen, "
                "or jack respectively) and s is the first letter of\nthe suit or c, s, h, d for clubs, spades, hearts, "
                "or diamonds respectively):")
            for req in selected.required_input.keys():
                selected.required_input[req] = input(req + ": ")
            #need to check input validity
            #this check should check the form (vs) as well as the fact that the card is possessed bu the current player
            result = selected.f(player, game_state, selected.required_input)
            if result == "":
                moved = True
            else:
                print("error: " + result)  # error message


"""
Class to represent a state transition. 
`next_state` is a string that is the name of the next state to go to
`guard` is a function taking in the game state that returns true if this state is a valid next state
`pre_transition_logic` is a function taking in game_state with any code that needs to be 
    executed before the next state occurs
"""


class Transition:
    def __init__(self, next_state, guard, pre_transition_logic):
        self.next_state = next_state
        self.guard = guard
        self.pre_transition_logic = pre_transition_logic

"""
Takes a string formatted as specified in the instructions to the player and returns a card object
"""

def getCard(str):
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
    return c

"""
Game object running a card game.
"""

class Game:
    game_state = {}

    def __init__(self, players, game_state, states, setup, finish):
        self.game_state = game_state  # state of game
        self.game_state[STATE_PLAYERS] = players  # players in game
        self.states = {s.name: s for s in states}
        self.setup = setup  # function to run start logic
        self.finish = finish  # function to run end logic

    def increment_turn(self):
        if STATE_TURNS in self.game_state:
            self.game_state[STATE_TURNS] = self.game_state[STATE_TURNS] + 1
        else:
            self.game_state[STATE_TURNS] = 1

    def start(self):
        self.setup(self)
        # game loop
        while not self.game_state[STATE_CURRENT_STATE].final_state:
            self.increment_turn()
            state = self.game_state[STATE_CURRENT_STATE]
            for p in self.game_state[STATE_PLAYERS]:
                clear_screen()
                state.move(p, self.game_state)
            for trans in state.transitions:
                if trans.guard(self.game_state):
                    trans.pre_transition_logic(self.game_state)
                    self.game_state[STATE_CURRENT_STATE] = self.states[trans.next_state]
        self.finish()


#    for i in range(4):
#        if i == 0:
#            game_state['players'][0].hand.extend(game_state['pass3s'][3])
#        else:
#            game_state['players'][i].hand.extend(game_state['pass3s'][i])

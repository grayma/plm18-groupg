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
        return str(self.value) + " " + self.suit
    
    def __eq__(self, other):
        if(str(self.suit) == str(other.suit) and str(self.value) == str(other.value)):
            return True
        else:
            return False
        
    def abbr(self):
        return (self.value[0] if not self.value == "10" else self.value) + self.suit[0]


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

        # figure out which move to use
        print("It is now %s's move, please pass the computer and press enter when %s has the computer." % (
            player.name, player.name))
        input()

        self.game_status(player, game_state)

        # make move
        moved = False
        while not moved:
            print("Available moves (type move name to use):")
            for mname in self.available_moves.keys():
                print(mname)
            selected = ""
            while selected not in self.available_moves.keys():
                selected = input("Please choose a valid move to execute: ")
            selected = self.available_moves[selected]
            if selected.required_input.keys():
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
    def __init__(self, source, dest, guard):
        self.source = source
        self.dest = dest
        self.guard = guard

"""
Game object running a card game.
"""
class Game:
    def __init__(self, gamespace, playerspace, states, transitions, setup, finish):
        self.gamespace = gamespace
        self.playerspace = playerspace
        self.states = states
        self.transitions = transitions
        self.setup = setup      
        self.finish = finish


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
            j = self.game_state['startPlayer']
            for i in range(1,(len(self.game_state[STATE_PLAYERS]) + 1)):
                clear_screen()
                p = self.game_state['players'][j - 1]
                state.move(p, self.game_state)
                j = j + 1
                if j > len(self.game_state[STATE_PLAYERS]):
                    j = 1

            #for p in self.game_state[STATE_PLAYERS]:
            #    clear_screen()
            #    state.move(p, self.game_state)


            for trans in state.transitions:
                if trans.guard(self.game_state):
                    trans.pre_transition_logic(self.game_state)
                    self.game_state[STATE_CURRENT_STATE] = self.states[trans.next_state]

        self.finish(self)

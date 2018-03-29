"""
Wrapper for a Player playing the game
"""
class Player:
    def __init__(self, name, index, score):
        self.name = name
        self.index = index
        self.score = 0
        self.playerspace = {}

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

class Pile:
    def __init__(self, cards):
        self.cards = cards

    def __repr__(self):
        return str(self.cards)

    def transfer_to(self, new_pile, subset):
        self.cards = [c for c in self.cards if c not in subset]
        new_pile.cards.extend(subset)
"""
Wrapper containing new and old game state and new and old player state to represent the
difference before and after a potential player's move.
`name` is the name of the move
`perform(Game)` is the function that actually executes the move, taking in a game and input. 
    Includes interaction with player. Returns "" if move successful, 
    an error message if needs to go again (rule break)
`required_args` dictionary representing required input for the move, game asks for key
"""

class Move:
    def __init__(self, name, perform, required_input):
        self.name = name
        self.f = f
        self.required_input = required_input


"""
Class representing a game's state machine
`name` name of the state the game is in
`status(player, state)` function taking a player and state showing player what info they need
`can_do(player, move)` function taking a player and a move and determining if they can perform it
`is_final` bool indicating whether or not game has finished 
"""
class State:
    def __init__(self, name, status, is_final):
        self.name = name
        self.status = status
        self.can_do = can_do
        self.is_final = is_final


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

`gamespace`
`states`
`start` start state
`transitions` transitions that can be made between game states
`setup(Game)` any setup to do before a game
`finish(Game)` any cleaning up to do after a game
"""
class Game:
    def __init__(self, gamespace, states, start, transitions, setup, finish):
        self.gamespace = gamespace
        self.playerspace = playerspace
        self.states = states
        self.transitions = transitions
        self.setup = setup      
        self.finish = finish

    def start(self):
        self.setup(self)
        # game loop

        """
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
        """
        self.finish(self)

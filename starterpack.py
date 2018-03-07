#Game
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

#Hearts State
#Main Deck main_deck [ card ]
#Game Played Cards played_cards int
#Hearts Broken? hearts_broken true/false
#
#Player Deck [ card ] 
#Player Cards Taken [ card ]
#Player Score [ card ]

"""
Game state dict constants
"""
STATE_PLAYERS = "players"
STATE_CURRENT_STATE = "state"
STATE_DECK = "deck"


"""
Wrapper for a Player playing the game
"""
class Player:
    def __init__(self, name, play):
        self.name = name

"""
Wrapper for a playing card
"""
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

"""
Wrapper contianing new and old game state and new and old player state to represent the
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
        self.available_moves = { m.name : m for m in available_moves }
        self.game_status = game_status
        self.final_state = final_state
    
    
    def move(self, player, game_state):
        "Makes a move for a player given the current game state."
        
        #figure out which move to use
        self.game_status(player, game_state)
        print("available moves (type move name to use):")
        for mname in self.available_moves.keys():
            print(mname)
        selected = ""
        while selected not in self.available_moves.keys:
            selected = input("please choose a valid move to execute: ")
            
        #make move
        moved = False
        while not moved:
            print("for this move we need the following: ")
            for req in selected.required_input.keys():
                selected.required_input[req] = input(req)
            result = selected.f(player, game_state, required_input)
            if result == "":
                moved = True
            else:
                print("error: " + result) #error message

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
Game object running a card game.
"""     
class Game:
    def __init__(self, players, game_state, states, setup, finish):
        self.players = players #players in game
        self.game_state = game_state #state of game
        self.states = { s.name : s for s in states }
        self.setup = setup #function to run start logic
        self.finish = finish #function to run end logic
        
        self.setup(self, game_state)
        
    def start(self):
        self.setup()
        
        while not self.game_state[STATE_CURRENT_STATE].final_state:
            state = self.game_state[STATE_CURRENT_STATE]
            for p in self.game_state[STATE_PLAYERS]:
                state.move(p, self.game_state)
            for trans in state.transitions:
                if trans.guard(self.game_state):
                    trans.pre_transition_logic(self.game_state)
                    self.game_state[STATE_CURRENT_STATE] = states[trans.next_state]
    
        self.finish()
        
        
#Standard Deck
suits = ['heart', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
deck = [Card(value, suit) for value in values for suit in suits]
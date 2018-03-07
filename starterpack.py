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

class Player:
    def __init__(self, name, play):
        self.name = name
        self.play = play #move function

"""
Wrapper for a playing card
"""
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

"""
Rules take in a key of the player/game state and then get the value at that key in the 
game state dictionary and then run the evaluation function on it.

`key` is the key of the value in the state dict to evaluate
`evaluate` is a function that takes in the state and key to evaluate
`gameState` is True if the rule evaluates game state, false if evaluates player state
"""
class Rule:
    def __init__(self, key, evaluate, gameState=True):
        self.key = key
        self.evaluate = evaluate
        self.gameState = gameState
            
"""
Wrapper contianing new and old game state and new and old player state to represent the
difference before and after a potential player's move.

`moveName` is the name of the move
`key` is the key in the state dict of what is to be changed
`delta` is a function that changes the game and player state based on the argument `arg`
"""
class Move:
    def __init__(self, moveName, key, delta, arg):
        self.moveName = moveName
        self.key = key
        self.delta = delta
        self.arg = arg
        
"""
Game object running a card game.
"""     
class Game:
    def __init__(self, players, deck, rules, setup, is_endgame):
        self.players = players #players in game
        self.deck = deck #card deck to use
        self.rules = rules #list of rules
        self.setup = setup #function to setup game
        self.is_endgame = is_endgame #function to evaluate if end reached
        
        self.state = {}
        self.players_state = { p.name : {} for p in players }
        
    def print_state(self):
        print(self.state)
        
    def print_players_state(self):
        print(self.players_state)
        
    def validate_move(self, player, move):
        print("Validating " + player.name + "'s move against rules.")
        return True #valid for now
        
    def update(self, player, move):
        print("Updating game state for " + player.name)
        
    def start(self):
        self.setup()
        for i in range(1,10):
            print("Turn " + str(i)) #start of turn
            for player in self.players:
                print(player.name + "'s turn")
                move = player.play() #make player move
                while not self.validate_move(player, move):
                    move = player.play()
                self.update(player, move)
            if is_endgame():
                break
        print("done")
        
        
#Standard Deck
suits = ['heart', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
deck = [Card(value, suit) for value in values for suit in suits]
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

import os

#clears screen, one way to have play on one computer
def clearscreen():
  os.system('cls||clear')
  
class Player:
    def __init__(self, name, play):
        self.name = name
        self.play = play #move function

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

#needs to be expanded on
class Rule:
    def __init__(self):
        pass
        
#some delta of the game state
class Move:
    def __init__(self, old_state, new_state, old_player_state, new_player_state):
        self.old_state = old_state
        self.new_state = new_state
        self.old_player_state = old_player_state
        self.new_player_state = new_player_state
            
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

#2 player hearts Deck (ONLY: Aces, 2's, 4's, 6's, 8's, 10's, queens)
values = ['ace', '2', '4', '6', '8', '10', 'queen']
smalldeck = [Card(value, suit) for value in values for suit in suits]

def generic_play():
    print("move made")
    return Move(None, None, None, None)
    
def generic_setup():
    return ""
    
def is_endgame():
    return False

p1 = Player("Matt", generic_play)
p2 = Player("Dan", generic_play)
r1 = Rule()
r2 = Rule()
g = Game([p1, p2], smalldeck, [r1, r2], generic_setup, is_endgame)
g.start() #run a generic game
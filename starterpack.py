from random import shuffle
suits = [ 'hearts', 'diamonds', 'spades', 'clubs' ]
suit_abbr_map = { 'h' : 'hearts', 'd' : 'diamonds', 's' : 'spades', 'c' : 'clubs' }
suit_map = { 'hearts' : 0, 'diamonds' : 1, 'spades' : 2, 'clubs' : 3 }
values = [ 'ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king' ]
values_abbr_map = { 'a' : 'ace', '2' : '2', '3' : '3', '4' : '4', '5' : '5', '6' : '6', '7' : '7', '8' : '8', '9' : '9', '10' : '10', 'j' : 'jack', 'q' : 'queen', 'k' : 'king' }
value_map = { '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'jack' : 11, 'queen' : 12, 'king' : 13, 'ace' : 14 }

def map_suit(abbr):
    return suit_abbr_map[abbr]

def map_value(card):
    return value_map[card.value]

def last(values):
    return values[-1]

class Player:
    """
    Wrapper for a Player playing the game
    """

    def __init__(self, name, index):
        """
        `name` name of player
        `index` order played in game
        """

        self.name = name
        self.index = index
        self.score = 0
        self.playerspace = {}
        self.hand = Pile([])

    def move(self, game):
        """
        `game` game being played, game.state contains state of game
        """
        state = game.state
        game.post("It's now {}'s' turn".format(self.name))
        state.status(self, game)
        selected = game.get(state.prompt_str)
        while selected not in state.moves or not state.moves[selected].canPerform(game, self):
            game.post("Move cannot be performed. Try again.")
            selected = game.get(state.prompt_str)
        state.moves[selected].perform(game, self)


class Card: 
    """
    Wrapper for a playing card
    """

    def __init__(self, value, suit):    
        """
        `value` value of the card
        `suit` suit of the card
        """

        self.value = value
        self.suit = suit

    def __repr__(self):
        return str(self.value) + "" + self.suit
    
    def __eq__(self, other):
        if(str(self.suit) == str(other.suit) and str(self.value) == str(other.value)):
            return True
        else:
            return False
        
    def abbr(self):
        return (self.value[0] if not self.value == "10" else self.value) + self.suit[0]

    @staticmethod
    def from_abbr(abbr):
        if len(abbr) == 3:
            return Card('10', suit_abbr_map[abbr[2]])
        return Card(values_abbr_map[abbr[0]], suit_abbr_map[abbr[1]])


class Pile:
    """
    Pile of cards allowing transfering between piles
    """

    def __init__(self, cards):
        """
        `cards` list of cards to instantiate this pile with
        """
        self.cards = cards

    def __repr__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
       return self.cards.__iter__()

    def __getitem__(self, index):
        return self.cards[index]
        
    def pop(self):
        return self.cards.pop()
        
    def remove(self, c):
        self.cards.remove(c)
    
    def is_empty(self):
        return not self.cards

    def transfer_to(self, new_pile, subset):
        """
        Transfers a subset of this pile to another pile.
        """
        for c in subset:
            if c not in self.cards:
                raise ValueError('"subset" of pile not actually a subset.')
        self.cards = [c for c in self.cards if c not in subset]
        new_pile.cards.extend(subset)
        
    def sort(self):
        """
        Sort the pile of cards
        """
        self.cards.sort(key = lambda x: value_map[x.value])
        self.cards.sort(key = lambda x: suit_map[x.suit])
        
class Deck(Pile):
    """
    Deck of cards allowing for dealing and shuffling
    """
    def __init__(self):
        cards = [Card(value, suit) for value in values for suit in suits]
        super(Deck, self).__init__(cards)
        
    def deal(self, players, per_player = 0):
        """
        Deal the cards in the deck to the given players
        """
        if not per_player:
            per_player = 52 // len(players)
        for p in players:
            self.transfer_to(p.hand, [self.cards[i] for i in range(per_player)])

    def shuffle(self):
        """
        Shuffle the cards in the deck
        """
        shuffle(self.cards)

class Move:
    """
    Wrapper containing new and old game state and new and old player state to represent the
    difference before and after a potential player's move.
    """
    
    def __init__(self, name, can_perform, logic, required):
        """ 
        `name` is the name of the move
        `can_perform(game, player)` logic determining if a player can perform this move
        `logic(Game, Player, input)` is the function that actually executes the move, taking in a game and input. 
            Includes interaction with player. Returns "" if move successful, 
            an error message if needs to go again (rule break)
        `required` dict containing necessary input for this move
        """

        self.name = name
        self.can_perform = can_perform
        self.logic = logic
        self.required = required
        
    def canPerform(self, game, player):
        return self.can_perform(game, player)

    def perform(self, game, player):
        self._getMoveInput(game)
        validate = self.logic(game, player, self.required)
        while validate != "":
            print(validate)
            self._getMoveInput(game)
            validate = self.logic(game, player, self.required)

    def _getMoveInput(self, game):
        for k, v in self.required.items():
            self.required[k] = game.get("Move requires {}: ".format(k))

class State:
    """
    Class representing a game's state machine 
    """

    def __init__(self, name, status, moves, logic, is_final, early_exit = None):
        """
        `name` name of the state the game is in
        `status(player, game)` function taking a player and game showing player what info they need
        `moves` list of moves available to this player at this point
        `logic(Game)` function performing any logic needed before the next state transition
        `is_final` bool indicating whether or not game has finished (aka final state)
        `early_exit(game)` function that checks if the state needs exit before all players have played
        """

        self.name = name
        self.status = status
        self.moves = { move.name : move for move in moves }
        self.prompt_str = "Please select a move from "
        for move in moves:
            self.prompt_str += ("'" + move.name + "'")
            if not move == last(moves): #add commas except after the last move.
                self.prompt_str += ", "
            else:
                self.prompt_str += ": "
        self.logic = logic
        self.is_final = is_final
        self.early_exit = early_exit

class Transition:
    """
    Class to represent a state transition. 
    """

    def __init__(self, source, dest, guard):
        """
        `source` from state
        `dest` to state
        `guard(Game)` true/false function evaluating the game to see if now is a valid time to take this transition
        """

        self.source = source
        self.dest = dest
        self.guard = guard

class Game:
    """
    Game object running a card game.
    """

    def __init__(self, players, gamespace, start_state, transitions, setup, finish, get, post):
        """
        `players` list of players playing the game
        `gamespace` dictionary containing any necessary game data
        `start_state` start state
        `transitions` transitions that can be made between game states
        `game_is_over(Game)` determines and returns winner player, None if no winner
        `setup(Game)` any setup to do before a game
        `finish(Game)` any cleaning up to do after a game
        `get(prompt)` function prompting the user for input
        `post(info)` function telling the user info
        """

        self.players = players
        self.gamespace = gamespace
        self.start_state = start_state
        self.transitions = transitions
        self.setup = setup      
        self.finish = finish
        self.get = get
        self.post = post

        self.turn = 1

    def perform_moves(self):
        for player in self.players:
            player.move(self)
            if self.state.early_exit and self.state.early_exit(self): #check for existence then run
                break

    def perform_transitions(self):
        for t in self.transitions:
            if t.guard(self) and t.source == self.state:
                self.state = t.dest
                break
        self.turn += 1 #turn is done, increment turn counter


    def start(self):
        self.setup(self)
        self.state = self.start_state

        #game loop
        while not self.state.is_final:
            self.perform_moves()
            self.state.logic(self) #run logic needed before state transition
            self.perform_transitions()

        self.finish(self)
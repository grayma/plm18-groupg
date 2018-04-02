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

    def move(self, game):
        """
        `game` game being played, game.state contains state of game
        """
        state = game.state
        game.post("It's now {}'s' turn".format(self.name))
        game.post(state.status(self, game))
        selected = game.get(state.prompt_str)
        while selected not in state.moves:
            selected = game.get(state.prompt_str)
        state.moves[selected].perform(game, player)


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
            return Card(10, abbr[2])
        return Card(abbr[0], abbr[1])


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

    def transfer_to(self, new_pile, subset):
        """
        Transfers a subset of this pile to another pile.
        """
        for c in subset:
            if c not in self.cards:
                raise ValueError('"subset" of pile not actually a subset.')
        self.cards = [c for c in self.cards if c not in subset]
        new_pile.cards.extend(subset)

class Move:
    """
    Wrapper containing new and old game state and new and old player state to represent the
    difference before and after a potential player's move.
    """
    
    def __init__(self, name, logic, required):
        """ 
        `name` is the name of the move
        `logic(Game, Player, input)` is the function that actually executes the move, taking in a game and input. 
            Includes interaction with player. Returns "" if move successful, 
            an error message if needs to go again (rule break)
        `required` dict containing necessary input for this move
        """

        self.name = name
        self.logic = logic
        self.required = required

    def perform(self, game, player):
        _getMoveInput()
        while not logic(game, player, self.required) == "":
            _getMoveInput()

    def _getMoveInput(self, game):
        for k, v in self.required.items():
            self.required[k] = game.get("Move requires {}".format(k))

class State:
    """
    Class representing a game's state machine 
    """

    def __init__(self, name, status, moves, is_final):
        """
        `name` name of the state the game is in
        `status(player, game)` function taking a player and game showing player what info they need
        `moves` list of moves available to this player at this point
        `is_final` bool indicating whether or not game has finished
        """

        self.name = name
        self.status = status
        self.moves = { move.name : move for move in moves }
        self.prompt_str = "Please select a move: "
        for move in moves:
            prompt_str += ("'" + move.name + "'")
            if not move == last(moves): #add commas except after the last move.
                prompt_str += ", "
            else:
                prompt_str += "."
        self.is_final = is_final



class Transition:
    """
    Class to represent a state transition. 
    """

    def __init__(self, source, dest, guard, logic):
        """
        `source` from state
        `dest` to state
        `guard(Game)` true/false function evaluating the game to see if now is a valid time to take this transition
        `logic(Game)` function performing any logic needed after this state transition
        """

        self.source = source
        self.dest = dest
        self.guard = guard
        self.logic = logic

class Game:
    """
    Game object running a card game.
    """

    def __init__(self, players, gamespace, start, transitions, game_is_over, setup, finish, get, post):
        """
        `players` list of players playing the game
        `gamespace` dictionary containing any necessary game data
        `start` start state
        `transitions` transitions that can be made between game states
        `game_is_over(Game)` determines and returns winner player, None if no winner
        `setup(Game)` any setup to do before a game
        `finish(Game)` any cleaning up to do after a game
        `get(prompt)` function prompting the user for input
        `post(info)` function telling the user info
        """

        self.players = players
        self.gamespace = gamespace
        self.start = start
        self.transitions = transitions
        self.game_is_over = game_is_over
        self.setup = setup      
        self.finish = finish
        self.get = get
        self.post = post

        self.turn = 1

    def start(self):
        self.setup(self)
        self.state = self.start

        # game loop
        done = None
        while not self.state.is_final:
            #perform moves
            for player in players:
                player.move(self)
                done = game_over(self)
                if done:
                    self.finish(self)
                    return

            self.turn += 1
            #state transitions
            for t in transitions:
                if t.guard(self):
                    self.state = t.dest
                    t.logic(Game)

        self.finish(self)
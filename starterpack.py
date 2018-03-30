class Player:
    """
    Wrapper for a Player playing the game
    """

    def __init__(self, name, index):
        """
        `name`
        `index` 
        """

        self.name = name
        self.index = index
        self.score = 0
        self.playerspace = {}

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
        return str(self.value) + " " + self.suit
    
    def __eq__(self, other):
        if(str(self.suit) == str(other.suit) and str(self.value) == str(other.value)):
            return True
        else:
            return False
        
    def abbr(self):
        return (self.value[0] if not self.value == "10" else self.value) + self.suit[0]

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
    
    def __init__(self, name, perform):
        """ 
        `name` is the name of the move
        `perform(Game)` is the function that actually executes the move, taking in a game and input. 
            Includes interaction with player. Returns "" if move successful, 
            an error message if needs to go again (rule break)
        """

        self.name = name
        self.perform = perform

class State:
    """
    Class representing a game's state machine 
    """

    def __init__(self, name, status, moves, is_final):
        """
        `name` name of the state the game is in
        `status(player, state)` function taking a player and state showing player what info they need
        `moves` list of moves available to this player at this point
        `is_final` bool indicating whether or not game has finished
        """

        self.name = name
        self.status = status
        self.moves = { move.name : move for move in moves }
        self.prompt_str = "Please select a move: "
        for move in moves:
            prompt_str += ("'" + move.name + "'")
            if not move == moves[-1]:
                prompt_str += ", "
            else:
                prompt_str += "."
        self.is_final = is_final

    def do_round(self, game):
        """
        Performs a round of game play for each player.
        """

        for player in game.players:
            game.post("It's now {}'s' turn".format(player.name))
            selected = game.request(self.prompt_str)
            while selected not in self.moves:
                selected = game.request(self.prompt_str)
            self.moves[selected].perform(game)



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

    def __init__(self, players, gamespace, start, transitions, setup, finish, get, post):
        """
        `players` list of players playing the game
        `gamespace` dictionary containing any necessary game data
        `start` start state
        `transitions` transitions that can be made between game states
        `setup(Game)` any setup to do before a game
        `finish(Game)` any cleaning up to do after a game
        `get(prompt)` function prompting the user for input
        `post(info)` function telling the user info
        """

        self.players = players
        self.gamespace = gamespace
        self.start = start
        self.transitions = transitions
        self.setup = setup      
        self.finish = finish
        self.get = get
        self.post = post

    def start(self):
        self.setup(self)
        state = self.start

        # game loop
        while not state.is_final:
            state.do_round()
            for t in transitions:
                if t.guard(self):
                    state = t.dest
                    t.logic(Game)

        self.finish(self)
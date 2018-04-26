from cards import *
from machine import *


def get_players(n, playerspace):
    """
    `n` number of players
    `playerspace()` function returning new playerspace for player
    """
    ps = []
    for i in range(n):
        name = ""
        while name == "":
            name = input("What's the name of player @ index {} (can't be empty): ".format(i))
        p = Player(name, i)
        p.playerspace = playerspace()
        ps.append(p)
    return ps


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
        self.revealed = [False, False, False, False, False, False]

    def all_revealed(self):
        x = True
        for i in self.revealed:
            if(i == False):
                x = False
        return x


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
            if self.state.early_exit and self.state.early_exit(self):  # check for existence then run
                break

    def perform_transitions(self):
        for t in self.transitions:
            if t.guard(self) and t.source == self.state:
                self.state = t.dest
                break
        self.turn += 1  # turn is done, increment turn counter

    def start(self):
        self.setup(self)
        self.state = self.start_state

        # game loop
        while not self.state.is_final:
            self.perform_moves()
            self.state.logic(self)  # run logic needed before state transition
            self.perform_transitions()

        self.finish(self)

from helper import last

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
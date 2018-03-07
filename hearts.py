from starterpack import *

#STATE_PLAYERS, STATE_CURRENT_STATE, STATE_DECK
STATE_TURN = "turns""
STATE_HEARTS = "hearts"
STATE_HEARTS_BROKEN = "broken"
STATE_PLAYED_CARDS = "played
PLAYER_STATE_SCORE = "score"

def get_highest_score(players):
    score = -1
    for p in players:
        if p[PLAYER_STATE_SCORE] > score:
            score = p.state[PLAYER_STATE_SCORE]
    return score

#moves
def pass3(player, state, input):
    pass
def play(player, state, input):
    pass
    

#transitions - happen by name
start_to_main = Transition("main", (lambda state: state[STATE_TURN] == 1))
main_to_broken = Transition("broken", (lambda state: state[STATE_HEARTS] == STATE_HEARTS_BROKEN))
broken_to_main = Transition("main", (lambda state: len(state[STATE_DECK]) == 0))
broken_to_finish = Transition("main", (lambda state: get_highest_score(state[STATE_PLAYERS]) >= 100)
 
#states
broken_transitions = [broken_to_main, broken_to_finish]
broken_moves = []
broken = State("broken hearts", broken_transitions, broken_rules, broken_moves)

main_transitions = [main_to_broken]
main_moves = []
main = State("main play", main_transitions, main_rules, main_moves)

start_transitions = [start_to_main]
start_moves = []
start = State("start", start_transitions, start_rules, start_moves)

finish = State("finish", None, None, None, True)
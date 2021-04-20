
import collections
import csv
Iterable = getattr(collections, 'Iterable', None)


# Checks if the state of the tic tac toe is winning or not.
# The board consists of these elements:
#   >   1 - First mover token
#   >   -1 - Second mover token
#   >   0 - Empty
# Returns:
#   >   1 if first mover wins.
#   >   -1 if second mover wins
#   >   0 if tie
#   >   None if intermediate state
win_positions = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
)


def checkWinning(state: Iterable):
    for pos in win_positions:
        if state[pos[0]] == state[pos[1]] == state[pos[2]] and state[pos[0]] != 0:
            return 1 if state[pos[0]] == 1 else -1
    if all(state):
        return 0
    return None


# Positive heuristic score favor the first mover. Negative heuristic favor the second mover
# The Larger the magnitude, the fewer turns needed to achieve win condition
state_scores = {}
state_first_mover_moves = {}
state_second_mover_moves = {}


def recurse(state: Iterable, turn: int, level: int):
    # Check winning case. The lower the level, the smaller the heuristic score
    is_win = checkWinning(state)
    if is_win is not None:
        state_scores[ tuple(state) ] = is_win / (9 ** level)
        return state_scores[ tuple(state) ]

    # No winning. Try to insert current turn - Backtracking.
    sum_of_scores = 0
    max_scores = [ None, [] ]          # [Score, index]. Records best move (if you are first mover)
    min_scores = [ None, [] ]          # [Score, index]. Records best move (if you are second mover)
    for i in range(9):
        if state[i]: continue                   # Occupied Grid

        # Backtracking (1) - Replace current grid with turn token
        prev = state[i]
        state[i] = turn

        # Memoization - Previously computed value
        if tuple(state) in state_scores:
            score = state_scores[ tuple(state) ]
        else:
            score = recurse(state, -turn, level+1 )
        # Backtracking (2) - Put back previous value once done
        state[i] = prev

        sum_of_scores += score
        if max_scores[0] is None or max_scores[0] < score:
            max_scores[0] = score
            max_scores[1].clear()
            max_scores[1].append(i)
        elif max_scores[0] == score:
            max_scores[1].append(i)

        if min_scores[0] is None or min_scores[0] > score:
            min_scores[0] = score
            min_scores[1].clear()
            min_scores[1].append(i)
        elif min_scores[0] == score:
            min_scores[1].append(i)

    state_scores[ tuple(state) ] = sum_of_scores

    state_second_mover_moves[ tuple(state) ] = min_scores[1]
    state_first_mover_moves[ tuple(state) ] = max_scores[1]
    return sum_of_scores


# Generate the scores and fill the next turn dictionaries
INIT_STATE = [0,0,0,0,0,0,0,0,0]
recurse( INIT_STATE, 1, 0 )


# Write a csv without heuristic records
with open('states_no_heuristic.csv', 'w', newline='') as csvfile:
    field_names = ('state', 'first_mover_opt_move', 'second_mover_opt_move')
    writer = csv.DictWriter(csvfile, fieldnames=field_names)

    writer.writeheader()

    states = state_first_mover_moves if len(state_first_mover_moves) > len(state_second_mover_moves) else state_second_mover_moves
    for s in states:
        writer.writerow({
            'state': s,
            'first_mover_opt_move': state_first_mover_moves.setdefault(s, ''),
            'second_mover_opt_move': state_second_mover_moves.setdefault(s, '')
        })


# Write a csv with heuristic records
with open('states.csv', 'w', newline='') as csvfile:
    field_names = ('state', 'state_heuristic', 'first_mover_opt_move', 'second_mover_opt_move')
    writer = csv.DictWriter(csvfile, fieldnames=field_names)

    writer.writeheader()

    for s in state_scores:
        writer.writerow({
            'state': s,
            'state_heuristic': state_scores[s],
            'first_mover_opt_move': state_first_mover_moves.setdefault(s, ''),
            'second_mover_opt_move': state_second_mover_moves.setdefault(s, '')
        })

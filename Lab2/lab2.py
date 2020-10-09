# MIT 6.034 Lab 2: Games
# Written by 6.034 staff

from game_api import *
from boards import *
from toytree import GAME1

INF = float('inf')


# Please see wiki lab page for full description of functions and API.

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    """Returns True if game is over, otherwise False."""
    if board.count_pieces() < 7:
        return False
    if board.count_pieces() == board.num_rows * board.num_cols:
        return True
    all_chains = board.get_all_chains()
    for chain in all_chains:
        if len(chain) >= 4:
            return True
    return False


def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
        return []
    next_boards = []
    for i in range(board.num_cols):
        if not board.is_column_full(i):
            new_board = board.add_piece(i)
            next_boards.append(new_board)
    return next_boards


def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if is_game_over_connectfour(board):
        winner = 0
        all_chains = board.get_all_chains()
        for chain in all_chains:
            if len(chain) >= 4:
                winner = winner + 1
        if winner == 0:
            return 0
        elif is_current_player_maximizer:
            return -1000
        else:
            return 1000


def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    if endgame_score_connectfour(board, is_current_player_maximizer) == -1000:
        return -1420 + 10 * board.count_pieces()
    elif endgame_score_connectfour(board, is_current_player_maximizer) == 1000:
        return 1420 - 10 * board.count_pieces()
    else:
        return 0


def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    current_chain = board.get_all_chains(current_player=True)
    other_chain = board.get_all_chains(current_player=False)
    score_current = 0
    score_other = 0
    for chain in current_chain:
        if len(chain) == 2:
            score_current = score_current + 10
        if len(chain) == 3:
            score_current = score_current + 20
    for chain in other_chain:
        if len(chain) == 2:
            score_other = score_other + 10
        if len(chain) == 3:
            score_other = score_other + 20
    if is_current_player_maximizer:
        return score_current - score_other
    else:
        return score_other - score_current


# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot=ConnectFourBoard(),
                                               is_game_over_fn=is_game_over_connectfour,
                                               generate_next_states_fn=next_boards_connectfour,
                                               endgame_score_fn=endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot=NEARLY_OVER,
                                      is_game_over_fn=is_game_over_connectfour,
                                      generate_next_states_fn=next_boards_connectfour,
                                      endgame_score_fn=endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot=BOARD_UHOH,
                               is_game_over_fn=is_game_over_connectfour,
                               generate_next_states_fn=next_boards_connectfour,
                               endgame_score_fn=endgame_score_connectfour_faster)


#### Part 2: Searching a Game Tree #############################################

# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state):
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    solution_list = []
    solution = [[state]]
    score = 0
    evals = 0
    best_path = []
    while (solution):
        path = solution.pop(0)
        last = path[-1]
        if last.is_game_over():
            solution_list.append(path)
            continue
        else:
            new_paths = []
            nodes = last.generate_next_states()
            for node in nodes:
                newpath = path.copy()
                newpath.append(node)
                new_paths.append(newpath)
            solution = new_paths + solution
    for solution in solution_list:
        evals = evals + 1
        compare_score = solution[-1].get_endgame_score()
        if score < compare_score:
            score = compare_score
            best_path = solution.copy()
        elif score == compare_score:
            if len(best_path) > len(solution):
                best_path = solution.copy()
    return best_path, score, evals


# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:

# pretty_print_dfs_type(dfs_maximizing(GAME1))


def minimax_endgame_search(state, maximize=True):
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    evals = 0
    best_path = None
    score = None
    if state.is_game_over():
        return [state], state.get_endgame_score(maximize), 1

    if maximize:
        for node in state.generate_next_states():
            compare = minimax_endgame_search(node, False)
            evals += compare[2]

            if best_path == None or compare[1] > score:
                best_path = [state] + compare[0]
                score = compare[1]
    else:
        for node in state.generate_next_states():
            compare = minimax_endgame_search(node, True)
            evals += compare[2]

            if best_path == None or compare[1] < score:
                best_path = [state] + compare[0]
                score = compare[1]

    return best_path, score, evals


# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:
# pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True):
    """Performs standard minimax search. Same return type as dfs_maximizing."""
    evals = 0
    best_path = None
    score = None

    if state.is_game_over():
        return [state], state.get_endgame_score(maximize), 1

    if depth_limit == 0:
        return [state], heuristic_fn(state.get_snapshot(), maximize), 1

    if maximize:
        for node in state.generate_next_states():
            depth = depth_limit - 1
            compare = minimax_search(node, heuristic_fn, depth, False)
            evals += compare[2]

            if best_path == None or compare[1] > score:
                best_path = [state] + compare[0]
                score = compare[1]
    else:
        for node in state.generate_next_states():
            depth = depth_limit - 1
            compare = minimax_search(node, heuristic_fn, depth, True)
            evals += compare[2]

            if best_path == None or compare[1] < score:
                best_path = [state] + compare[0]
                score = compare[1]

    return best_path, score, evals


# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:
# pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))

def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True):
    """"Performs minimax with alpha-beta pruning. Same return type
    as dfs_maximizing."""
    evals = 0
    best_path = None
    score = None

    if state.is_game_over():
        return [state], state.get_endgame_score(maximize), 1

    if depth_limit == 0:
        return [state], heuristic_fn(state.get_snapshot(), maximize), 1

    if maximize:
        for node in state.generate_next_states():
            depth = depth_limit - 1
            compare = minimax_search_alphabeta(node, alpha, beta, heuristic_fn, depth, False)
            evals += compare[2]

            if best_path == None or compare[1] > score:
                best_path = [state] + compare[0]
                score = compare[1]
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    return best_path, alpha, evals
    else:
        for node in state.generate_next_states():
            depth = depth_limit - 1
            compare = minimax_search_alphabeta(node, alpha, beta,heuristic_fn, depth, True)
            evals += compare[2]

            if best_path == None or compare[1] < score:
                best_path = [state] + compare[0]
                score = compare[1]
                if beta > score:
                    beta = score
                if alpha >= beta:
                    return best_path, beta, evals

    return best_path, score, evals


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

# pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))

def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True):
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime = AnytimeValue()
    for d in range(1, depth_limit + 1):
        result = minimax_search_alphabeta(state, -INF, INF, heuristic_fn, d, maximize)
        anytime.set_value(result)
    return anytime


# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

# progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


# Progressive deepening is NOT optional. However, you may find that 
#  the tests for progressive deepening take a long time. If you would
#  like to temporarily bypass them, set this variable False. You will,
#  of course, need to set this back to True to pass all of the local
#  and online tests.
TEST_PROGRESSIVE_DEEPENING = True
if not TEST_PROGRESSIVE_DEEPENING:
    def not_implemented(*args): raise NotImplementedError


    progressive_deepening = not_implemented

#### Part 3: Multiple Choice ###################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'

#### SURVEY ###################################################

NAME = "Vignesh Gopalakrishnan"""
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 12
WHAT_I_FOUND_INTERESTING = "The concepts involved in adversarial search, actually doing the trees and suchlike"
WHAT_I_FOUND_BORING = "Actual code implementation with the function recursions. Eventually, I figured out how to do the path correctly one day later - append vs +[list] ARGHHHHHH. I'M SO SAD :((((((("
SUGGESTIONS = "Less complicated ask for minimax implementation, maybe"

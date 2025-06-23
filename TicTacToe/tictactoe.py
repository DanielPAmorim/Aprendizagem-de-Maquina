"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not isinstance(action, tuple) or len(action) != 2 or \
       not all(isinstance(coord, int) and 0 <= coord <= 2 for coord in action):
        raise ValueError("Invalid action format. Action must be a tuple (i, j) with 0 <= i, j <= 2.")

    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid action: Cell is already occupied.")

    new_board = copy.deepcopy(board)
    current_player = player(board)
    new_board[i][j] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O

    # Check columns
    for j in range(3):
        if all(board[i][j] == X for i in range(3)):
            return X
        elif all(board[i][j] == O for i in range(3)):
            return O

    # Check diagonals
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X) or \
       (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return X
    elif (board[0][0] == O and board[1][1] == O and board[2][2] == O) or \
         (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    # Check if all cells are filled
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        return max_value(board)[1]  # Return the action
    else:
        return min_value(board)[1]  # Return the action

def max_value(board):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    best_action = None
    for action in actions(board):
        new_v, _ = min_value(result(board, action))
        if new_v > v:
            v = new_v
            best_action = action
    return v, best_action


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_action = None
    for action in actions(board):
        new_v, _ = max_value(result(board, action))
        if new_v < v:
            v = new_v
            best_action = action
    return v, best_action

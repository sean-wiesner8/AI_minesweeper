from sympy import *
import numpy as np
import math
from collections import deque

# represents the knowledge base of the AI, so that moves are not duplicated
mines = set()
empty = set()

# store moves as a tripple - (opp, r, c) - where opp is "flag" or "mine" and
# and r and c represent coordinates row and columns respectively
queue = deque()

# the change in tile for each of the 8 surrounding tiles

coordinates = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}

""" given an n x n board state, create an n^2 x n^2 + 1 matrix representation. Each
row index and col index corresponds to a particular tile. For example a tile index
with (row_index, col_index) in board_state would map to row_index * column_size
+ col_index on either axis. For each row, if the corresponding tile is opened
and has a postive surrounding mine count, mark each of the unopened tiles as 1 
in the corresponding column index. The final row of the matrix should be equal to
the amount of surrounding mines if the tile has been opened."""


def to_matrix(board_state):
    tile_count = len(board_state) ** 2
    board_rep = np.zeros((tile_count, tile_count + 1))
    col_size = len(board_state[0])
    row_size = len(board_state)
    for r in range(row_size):
        for c in range(col_size):
            if board_state[r][c] > 0:
                board_rep[c + r * col_size][tile_count] = board_state[r][c]
                for i, j in coordinates:
                    if (
                        r + i >= 0
                        and j + c >= 0
                        and j + c < col_size
                        and r + i < row_size
                        and board_state[r + i][c + j] == -1
                    ):
                        board_rep[c + r * col_size][(c + j) + (r + i) * col_size] = 1
                    elif (
                        r + i >= 0
                        and j + c >= 0
                        and j + c < col_size
                        and r + i < row_size
                        and board_state[r + i][c + j] == -2
                    ):
                        board_rep[c + r * col_size][tile_count] -= 1
    return board_rep


"""For the row reduced version of the matrix representation of board_state,
analyze each row to see if any certain moves can be made. A row is analyzed
by seeing if the final column index is equal to the maximum or minimum of this equation.
If it is equal to the maximum, positive tiles are mines and negative tiles are empty.
If it is equal to the minimum, postive tiles are empty and negative tiles are mines.
The given information should be added to queue, which represents certain moves. Additionally, 
the AI knowledge base (the sets mines and empty) should be updated."""


def analyze_matrix(board_rep, board_state):
    tile_count = len(board_state) ** 2
    for r in range(tile_count):
        maximum = 0
        minimum = 0
        for c in range(tile_count):
            if board_rep[r, c] > 0:
                maximum += board_rep[r, c]
            else:
                minimum += board_rep[r, c]
        if maximum == board_rep[r, tile_count]:
            for c in range(tile_count):
                i, j = c // len(board_state), c % len(board_state)
                if board_rep[r, c] > 0:
                    if (i, j) not in mines:
                        queue.append(("flag", i, j))
                        mines.add((i, j))
                elif board_rep[r, c] < 0:
                    if (i, j) not in empty:
                        queue.append(("open", i, j))
                        empty.add((i, j))
        elif minimum == board_rep[r, tile_count]:
            for c in range(tile_count):
                i, j = c // len(board_state), c % len(board_state)
                if board_rep[r, c] > 0:
                    if (i, j) not in empty:
                        queue.append(("open", i, j))
                        empty.add((i, j))
                elif board_rep[r, c] < 0 and (i, j) not in mines:
                    queue.append(("flag", i, j))
                    mines.add((i, j))


"""Given a board_state, run the CSP solver"""


def CSP_solver(board_state):
    # create a matrix representation of the board_state
    board_rep = to_matrix(board_state)

    # row reduce the board representation
    board_rep = Matrix(board_rep)
    board_rep.rref()

    # determine flag and move operations from the row reduced board representation
    analyze_matrix(board_rep, board_state)


"""Given a board_state, run the single point solver. This consists of checking
 whether given the surrounding mine count of a tile, can we reveals known mines 
 or bombs. We may flag tiles if the mine count == unopened tile count, and we
 may open tiles if the mine count == flagged count"""


def SP_solver(board_state):
    # mark known mines and open known tiles
    col_size = len(board_state[0])
    row_size = len(board_state)
    for r in range(row_size):
        for c in range(col_size):
            mine_count = board_state[r][c]
            unopened_tiles = []
            flaged_tiles = []
            if mine_count > 0:
                for i, j in coordinates:
                    if (
                        r + i >= 0
                        and j + c >= 0
                        and j + c < col_size
                        and r + i < row_size
                    ):
                        if board_state[r + i][j + c] == -1:
                            unopened_tiles.append((r + i, j + c))
                        elif board_state[r + i][j + c] == -2:
                            flaged_tiles.append((r + i, j + c))
                if len(flaged_tiles) == mine_count:
                    for x, y in unopened_tiles:
                        if (x, y) not in empty:
                            queue.append(("open", x, y))
                            empty.add((x, y))
                elif len(unopened_tiles) + len(flaged_tiles) == mine_count:
                    for x, y in unopened_tiles:
                        if (x, y) not in mines:
                            queue.append(("flag", x, y))
                            mines.add((x, y))


"""Given a board_state, choose a random unopened tile """


def random_move(board_state):
    unopened = np.argwhere(board_state == -1)
    index = np.random.choice(len(unopened))
    r, c = unopened[index][0], unopened[index][1]
    empty.add((r, c))
    print("random!")
    return ("open", r, c)


"""Given a board_state and bomb_count, output the tile with the lowest probability """


def select_tile_with_lowest_probability(board_state, bomb_count):
    pass


"""Given a board_state output an opp: open or flag, an a coordinate r, c to do such operation """


def ai_heuristic_logic(board_state, first_move, bomb_count):
    if first_move:
        while queue:
            queue.pop()
        mines.clear()
        empty.clear()

    # If a move remains from last AI call, return move
    if queue:
        return queue.popleft()

    # certain_move shows how we developed the AI's certain move strategy
    # 0 is the basic strategy where it makes a move based on information at a single point
    # 1 takes into account all the information we know and creates a constraint satisfaction problem
    certain_move = 0
    if certain_move == 0:
        SP_solver(board_state)
    elif certain_move == 1:
        CSP_solver(board_state)

    # If trivial move was found, make trivial move
    if queue:
        return queue.popleft()

    # uncertain_move shows how we developed the AI's uncertain move strategy
    # 0 is the basic strategy where it makes a random move if there are no certain moves
    # 1 takes into account the probability of each tile and returns the one with lowest chance of being a mine
    # 2 adds a distance heuristic
    uncertain_move = 0

    # if no queue chose a random unopened tile
    if uncertain_move == 0:
        return random_move(board_state)
    elif uncertain_move == 1:
        r, c = select_tile_with_lowest_probability(board_state, bomb_count)
        return ("open", r, c)

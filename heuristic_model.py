import sympy
import numpy as np
import random
from collections import deque

# store operations
queue = deque()

# board state constants
unopened = -1
flaged = -2

# the change in tile for each of the 8 surrounding tiles

coordinates = {(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1,  0), (1, 1)}

# given a board_state output an opp: open or flag, an a coordinate to do such operation


def ai_heuristic_logic(board_state):
    if queue:
        return queue.popleft()

    tile_count = len(board_state)**2
    board_rep = np.zeroes(tile_count, tile_count+1)
    col_size = len(board_state)
    row_size = len(board_state[0])
    for r, row in enumerate(board_state):
        for c, tile_state in enumerate(row):
            if tile_state > unopened+1:
                board_rep[c + r * col_size][tile_count] = tile_state
                for i, j in coordinates:
                    if r + i >= 0 and j+c >= 0 and j+c < col_size and r+i < row_size:
                        if (board_state[r+i][c+j] == unopened):
                            board_rep[c + r *
                                      col_size][(c+j) + (r+i) * col_size] = 1

    board_rep.rref()

    # fill queue

    # output first move, update queue
    if queue:
        return queue.popleft()

    r, c = random.randint(0, len(board_state[0])), random.randint(
        0, len(board_state))
    # make a random move
    while (board_state[r][c] != unopened):
        r, c = random.randint(0, len(board_state[0])), random.randint(
            0, len(board_state))

    return ("open", r, c)

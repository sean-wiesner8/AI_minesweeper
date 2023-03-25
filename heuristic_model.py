import sympy
import numpy as np
import random

# store operations
queue = []

# the change in tile for each of the 8 surrounding tiles

coordinates = {(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1,  0), (1, 1)}

# given a board_state output an opp: open or flag, an a coordinate to do such operation


def ai_heuristic_logic(board_state):
    if len(queue) != 0:
        move = queue[0]
        queue = queue[1:]
        return move

    tile_count = len(board_state)**2
    board_rep = np.zeroes(tile_count, tile_count+1)
    col_size = len(board_state)
    row_size = len(board_state[0])
    for col in range(col_size):
        for row in range(row_size):
            if (board_state[r][c] > 0):
                for r, c in coordinates:
                    if row+r >= 0 and col+c >= 0 and row+r < col_size and row_size:
                        if (board_state[r+row][c+col] == -1):
                            board_rep[row+row_size *
                                      col][(row+r)+(row_size)*(col+c)] = 1

    board_rep[:][tile_count] = np.sum(board_rep, axis=1)
    board_rep.rref()

    # fill queue

    # output first move, update queue
    if len(queue) != 0:
        move = queue[0]
        queue = queue[1:]
        return move
    # make a random move
    else:
        return ("open", random.randint(0, len(board_state[0])), random.randint(0, len(board_state)))

import random
import numpy as np
import heuristic_model
import time
import sys

# Raise recursion limit to avoid RecursionError on bigger boards
sys.setrecursionlimit(2**16)

# initalized after the first move, board represents the data hidden to the user.
# Each board is a certain size and has a certain mine count
# board constants
mine = 1
empty_tile = 0

# initalized at the begining of the game, board state represents the data the
# user can see.
# board state constants
unopened = -1
flaged = -2


# the change in tile for each of the 8 surrounding tiles
coordinates = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}

"""initalize minesweeper with a [size] x [size] board and mine count [mine]. 
does not allow a bomb to be initated at (r,c)"""


def init_board(board_height, board_width, mine, r, c):
    board = np.zeros((board_height, board_width))
    first_move = r * board_width + c
    left = list(range(0, first_move))
    right = list(range(first_move + 1, board_width * board_height))
    bombs = random.sample(left + right, mine)
    board[np.unravel_index(bombs, board.shape)] = 1
    return board


"""initalize minesweeper with a [size] x [size] board state where all tiles are unopened"""


def init_board_state(board_height, board_width):
    board_state = np.full((board_height, board_width), unopened)
    return board_state


"""open a tile if not flagged. In board state update the tile with the amount of surrounding bombs.
If there are no surrounding bombs, open the eight neighbor tiles."""


def open_tile(board_state, board, row, col):
    if board_state[row][col] != flaged:
        board_state[row][col] = count_surrounding_bombs(board, row, col)
        if board_state[row][col] == 0 and board[row][col] != mine:
            for r, c in coordinates:
                if (
                    row + r >= 0
                    and col + c >= 0
                    and row + r < len(board)
                    and col + c < len(board[0])
                ):
                    if board_state[row + r][col + c] == unopened:
                        board_state = open_tile(board_state, board, row + r, col + c)
    return board_state


"""flag a single tile if it is unflagged and unopened. If flagged, unflag."""


def flag_tile(board_state, row, col):
    if board_state[row][col] != flaged and board_state[row][col] < 0:
        board_state[row][col] = flaged
    elif board_state[row][col] == flaged:
        board_state[row][col] = unopened
    return board_state


"""Check how many bombs are in the surrounding eight tiles around a particular tile"""


def count_surrounding_bombs(board, row, col):
    count = 0
    for r, c in coordinates:
        if (
            row + r >= 0
            and col + c >= 0
            and row + r < len(board)
            and col + c < len(board[0])
            and board[row + r][col + c] == mine
        ):
            count += 1
    return count


"""check to see if game has been lost, where losing is defined as a mine being opened."""


def game_lost(board, board_state):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == mine and board_state[i][j] >= 0:
                return True
    return False


"""check to see if game has been won, where wining is defined as all empty tiles have been opened."""


def game_won(board_state, bomb_count):
    open_tiles = 0
    for i in range(len(board_state)):
        for j in range(len(board_state[0])):
            if board_state[i][j] >= 0:
                open_tiles += 1
    return open_tiles == len(board_state) * len(board_state[0]) - bomb_count


"""print a row of the game board to the console."""


def print_row(board, board_state, row_num):
    for c in range(len(board[0])):
        if board_state[row_num][c] == unopened:
            print("-", end=" ")
        elif board_state[row_num][c] == flaged:
            print("f", end=" ")
        elif board[row_num][c] == mine:
            print("m", end=" ")
        else:
            print(board_state[row_num][c], end=" ")


"""print the game board to the console."""


def print_board(board, board_state):
    for r in range(len(board)):
        print_row(board, board_state, r)
        print()


"""game loop for minesweeper game mode."""


def printed_game_loop(mode, bomb_count, board_height, board_width):
    board = np.zeros((board_height, board_width))
    board_state = init_board_state(board_height, board_width)
    move_count = 0
    first_move = True
    while not game_won(board_state, bomb_count) and not game_lost(board, board_state):
        if mode == "human":
            read = input()
            read_split = read.split()
            if (
                len(read_split) == 3
                and type(read_split[0]) == str
                and read_split[1].isdigit()
                and read_split[1].isdigit()
            ):
                opp = read_split[0]
                r = int(read_split[1])
                c = int(read_split[2])
                if r < 0 or c < 0 or r >= board_height or c >= board_height:
                    print("Out of bounds")
                    continue
        else:
            opp, r, c = heuristic_model.ai_heuristic_logic(
                board_state, first_move, bomb_count
            )
        if opp == "open":
            if first_move:
                board = init_board(board_height, board_width, bomb_count, r, c)
                first_move = False
            board_state = open_tile(board_state, board, r, c)
        if opp == "flag":
            board_state = flag_tile(board_state, r, c)
        print()
        move_count += 1
        print("Move: " + opp + " " + str(r) + " " + str(c))
        print_board(board, board_state)
    if game_lost(board, board_state):
        print("you lost")
        return False
    else:
        print("you won")
        return True


"""output the number of wins for a given number of trials"""


def trials():
    board_width = int(input("Enter board width: "))
    board_height = int(input("Enter board height: "))
    bomb_count = int(input("Enter bomb count: "))
    iterations = int(input("input number of trial iteration: "))
    count = iterations

    start_time = time.time()
    win = 0
    while iterations > 0:
        if printed_game_loop("ai", bomb_count, board_height, board_width):
            win += 1
        iterations -= 1
    end_time = time.time()
    print("Trials: " + str(count))
    print("Wins: " + str(win))
    print("Sucess Rate: " + str(win / count))
    print("elapsed time: " + str(end_time - start_time))


def main():
    trials()


if __name__ == "__main__":
    main()

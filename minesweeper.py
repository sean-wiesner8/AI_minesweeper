import random
import numpy as np
import heuristic_model

# board constants
mine = 1
empty_tile = 0

# board state constants
unopened = -1
flaged = -2

# the change in tile for each of the 8 surrounding tiles
coordinates = {(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1,  0), (1, 1)}

# initalize minesweeper with a [size] x [size] board and mine count [mine]


def init_board(size, mine):
    board = np.zeros((size, size))
    bombs = random.sample(range(np.square(size)), mine)
    board[np.unravel_index(bombs, board.shape)] = 1
    return board

# initalize minesweeper with a [size] x [size] board where all tiles are unopened


def init_board_state(size):
    board_state = np.full((size, size), -1)
    return board_state

# open a tile if not flagged. If bomb, mark lost condition.


def open_tile(board_state, board, row, col):
    if board_state[row][col] != flaged:
        board_state[row][col] = count_surrounding_bombs(board, row, col)
        if board_state[row][col] == 0:
            for r, c in coordinates:
                if row+r >= 0 and col+c >= 0 and row+r < len(board) and col+c < len(board[0]):
                    if board_state[row+r][col+c] == unopened:
                        board_state = open_tile(
                            board_state, board, row+r, col+c)
    return board_state

# flag a single tile if it is unflagged and unopened. If flagged unflag


def flag_tile(board_state, row, col):
    if board_state[row][col] != flaged and board_state[row][col] < 0:
        board_state[row][col] = flaged
    elif board_state[row][col] == flaged:
        board_state[row][col] = unopened
    return board_state

# check how many bombs are surrounding a particular tile


def count_surrounding_bombs(board, row, col):
    count = 0
    for r, c in coordinates:
        if row+r >= 0 and col+c >= 0 and row+r < len(board) and col+c < len(board[0]):
            if board[row+r][col+c] == mine:
                count += 1
    return count

# check to see if game has been lost


def game_lost(board, board_state):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == mine and board_state[i][j] >= 0:
                return True
    return False

# check to see if game has been won


def game_won(board_state, bomb_count):
    open_tiles = 0
    for i in range(len(board_state)):
        for j in range(len(board_state[0])):
            if board_state[i][j] < 0:
                open_tiles += 1
    return open_tiles == len(board_state)*len(board_state[0]) - bomb_count


# print a row of the game board to the console


def print_row(board, board_state, row_num):
    for c in range(len(board[0])):
        if board_state[row_num][c] == unopened:
            print('-', end=" ")
        elif board_state[row_num][c] == flaged:
            print('f', end=" ")
        elif board[row_num][c] == mine:
            print('m', end=" ")
        else:
            print(board_state[row_num][c], end=" ")


# print the game board to the console

def print_board(board, board_state):
    for r in range(len(board)):
        print_row(board, board_state, r)
        print()

# game loop for minesweeper game mode


def printed_game_loop(mode):
    bomb_count = 10
    board_size = 15
    board = init_board(board_size, bomb_count)
    board_state = init_board_state(board_size)
    move_count = 0
    while not game_lost(board, board_state) or game_won(board_state, bomb_count):
        print("Move " + str(move_count))
        print_board(board, board_state)
        if mode == "human":
            read = input()
            read_split = read.split()
            if len(read_split) == 3 and type(read_split[0]) == str and read_split[1].isdigit() and read_split[1].isdigit():
                opp = read_split[0]
                r = int(read_split[1])
                c = int(read_split[2])
        else:
            opp, r, c = heuristic_model.ai_heuristic_logic(board_state)
        if opp == "open":
            board_state = open_tile(board_state, board, r, c)
        if opp == "flag":
            board_state = flag_tile(board_state, r, c)
        print()
        move_count += 1
    if game_lost(board, board_state):
        print("you lost")
        return False
    else:
        print("you won")
        return True


# output the number of wins for a given number of trials
def trials(count):
    win = 0
    while count > 0:
        if printed_game_loop("ai"):
            win += 1
    print("Trials: " + count)
    print("Wins: " + win)
    print("Sucess Rate: " + win/count)


printed_game_loop("human")

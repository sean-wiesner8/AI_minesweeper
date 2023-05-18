import random
import numpy as np
import pandas as pd
import minesweeper

class DQEnvironment(object):
    def __init__(self, bomb_count, board_size):
        self.board_size = board_size
        self.bomb_count = bomb_count
        first_r = random.randint(1, board_size - 1)
        first_c = random.randint(1, board_size - 1)
        self.board = np.zeros((board_size, board_size))
        self.init_board_state = minesweeper.open_tile(minesweeper.init_board_state(board_size), self.board, first_r, first_c)
        self.rewards = {'win':1,'lose':-0.5,'progress':0.1,'guess':0.01, 'no_progress': -1e10}
        self.UNOPENED = -1
        self.FLAGGED = -2
        self.OPENED = range(9)
        self.MINE = 1
        self.EMPTY_TILE = 0
        self.wins = 0
        self.total = 0
        self.progress = 0
        self.total_moves = 0

    def is_guess(self, r, c, old_board_state):
        board_size = self.board_size
        coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (1, -1), (-1, 1)]
        for dr, dc in coordinates:
            new_r = r + dr
            new_c = c + dc
            if new_r < board_size and new_r >= 0 and new_c < board_size and new_c >= 0 and old_board_state[new_r][new_c] in self.OPENED:
                return False
        return True

    def step(self, action):
        old_board_state = self.board_state
        done = False
        action_row = action // self.board_size
        action_col = action % self.board_size
        new_board_state = minesweeper.open_tile(old_board_state, self.board, action_row, action_col)
        self.board_state = new_board_state
        guessed = self.is_guess(action_row, action_col, old_board_state)

        #lose condition
        if self.board[action_row][action_col] == self.MINE:
            reward = self.rewards['lose']
            done = True
            self.total += 1
        #win condition
        elif np.sum(new_board_state in self.OPENED) == self.board_size - self.bomb_count:
            reward = self.rewards['win']
            done = True
            self.wins += 1
            self.total += 1
            self.progress += 1
        #no progress condition
        elif old_board_state[action_row][action_col] in self.OPENED:
            reward = self.rewards['no_progress']
        #guess condition
        elif guessed:
            reward = self.rewards['guess']
            self.progress += 1
        #progress condition
        else:
            reward = self.rewards['progress']
            self.progress += 1
        self.total_moves += 1
        return self.board_state, reward, done
    
    def reset(self):
        first_r = random.randint(1, self.board_size - 1)
        first_c = random.randint(1, self.board_size - 1)
        self.board = minesweeper.init_board(self.board_size, self.bomb_count, first_r, first_c)
        self.init_board_state = minesweeper.open_tile(minesweeper.init_board_state(self.board_size), self.board, first_r, first_c)






    



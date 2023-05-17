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
        self.board = minesweeper.init_board(self.board_size, self.bomb_count, first_r, first_c)
        self.init_board_state = minesweeper.open_tile(minesweeper.init_board_state(board_size), self.board, first_r, first_c)
        #TODO Initialize other fields like rewards. There are probably others that I'm not aware of right now

    



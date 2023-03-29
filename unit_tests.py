import heuristic_model
import minesweeper
import numpy as np
import unittest


class TestInitBoard(unittest.TestCase):

    def test_init_board_10(self):
        init_board = minesweeper.init_board(10, 3, 4, 4)
        unique, counts = np.unique(init_board, return_counts=True)
        counter = dict(zip(unique, counts))
        for _ in range(100):
            self.assertEqual(
                counter[1], 3, "incorrect number of mines in initial board state")
            self.assertEqual(init_board[4, 4], 0, "start tile should be empty")

    def test_init_board_state():
        
        pass

    def test_open_tile():
        pass

    def test_flag_tile():
        pass

    def test_count_surrounding_bombs():
        pass

    def test_game_lost():
        pass

    def game_game_won():
        pass

    def test_ai_heuristic_logic():
        pass


unittest.main()

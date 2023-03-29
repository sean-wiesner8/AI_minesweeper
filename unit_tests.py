import heuristic_model
import minesweeper
import numpy as np
import unittest


class TestInitBoard(unittest.TestCase):

    def test_init_board_10(self):
        for _ in range(100):
            init_board = minesweeper.init_board(10, 3, 4, 4)
            unique, counts = np.unique(init_board, return_counts=True)
            counter = dict(zip(unique, counts))
            self.assertEqual(
                counter[1], 3, "incorrect number of mines in initial board state")
            self.assertEqual(init_board[4, 4], 0, "start tile should be empty")

    def test_init_board_state(self):
        init_board_state = minesweeper.init_board_state(5)
        self.assertEqual(init_board_state.shape, (5, 5),
                         "board state is initalized to inccorect size")
        self.assertEqual(np.all(init_board_state), True,
                         "when initalized board state has an open tile")

    def test_open_tile(self):
        pass

    def test_flag_tile(self):
        pass

    def test_count_surrounding_bombs(self):
        pass

    def test_game_lost(self):
        pass

    def game_game_won(self):
        pass

    def test_to_matrix(self):
        pass

    def test_analyze_matrix(self):
        pass

    def test_ai_heuristic_logic(self):
        pass

    def test_trials(self):
        pass


unittest.main()

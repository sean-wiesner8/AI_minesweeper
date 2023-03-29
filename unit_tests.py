import heuristic_model
import minesweeper
import numpy as np
import unittest


def init_test_board(size, m_indices):
    init_board = np.zeros((size, size))
    for i, j in m_indices:
        init_board[i][j] = 1
    return init_board


def init_test_board_state(size, f_indices, o_indices):
    board_state = minesweeper.init_board_state(size)
    for i, j in f_indices:
        board_state[i][j] = -2
    for i, j in o_indices:
        board_state[i][j] = -1
    return board_state


class TestInitBoard(unittest.TestCase):

    def test_init_board_10(self):
        init_board = minesweeper.init_board(10, 3, 4, 4)
        unique, counts = np.unique(init_board, return_counts=True)
        counter = dict(zip(unique, counts))
        for _ in range(100):
            self.assertEqual(
                counter[1], 3, "incorrect number of mines in initial board state")
            self.assertEqual(init_board[4, 4], 0, "start tile should be empty")

    def test_init_board_state(self):

        pass

    def test_open_tile(self):
        # for size in range(10, 100):
        #     f_indices = [(size / 2, (size / 2) + 1)] #1 arbitrary flag location
        #     o_indices = [((size / 2) - 1, (size / 2) - 1), ((size / 2) - 2, (size / 2) - 2)] #2 arbitrary opened tiles
        #     board_state = init_test_board_state(size, f_indices, o_indices)
        #     f_index = f_indices[0]
        #     o_index1 = o_indices[0]
        #     o_index2 = o_indices[1]
        pass

    def test_flag_tile(self):
        pass

    def test_count_surrounding_bombs(self):
        m_indices = [(0, 0), (6, 6), (4, 5), (5, 6)]
        board = init_test_board(10, m_indices)
        actual_val = minesweeper.count_surrounding_bombs(board, 5, 5)
        expected_val = 3
        self.assertEqual(actual_val, expected_val,
                         f"expected {expected_val} but got {actual_val}")
        actual_val2 = minesweeper.count_surrounding_bombs(board, 2, 2)
        expected_val2 = 0
        self.assertEqual(actual_val2, expected_val2,
                         f"expected {expected_val2} but got {actual_val2}")
        actual_val3 = minesweeper.count_surrounding_bombs(board, 1, 0)
        expected_val3 = 1
        self.assertEqual(actual_val3, expected_val3,
                         f"expected {expected_val3} but got {actual_val3}")

    def test_game_lost(self):
        pass

    def game_game_won(self):
        pass

    def test_ai_heuristic_logic(self):
        pass


unittest.main()

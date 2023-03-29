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
        for _ in range(100):
            init_board = minesweeper.init_board(10, 3, 4, 4)
            unique, counts = np.unique(init_board, return_counts=True)
            counter = dict(zip(unique, counts))
            self.assertEqual(
                counter[1], 3, "incorrect number of mines in initial board state"
            )
            self.assertEqual(init_board[4, 4], 0, "start tile should be empty")


class TestInitBoardState(unittest.TestCase):
    def test_init_board_state(self):
        init_board_state = minesweeper.init_board_state(5)
        self.assertEqual(
            init_board_state.shape,
            (5, 5),
            "board state is initalized to inccorect size",
        )
        self.assertEqual(
            np.all(init_board_state),
            True,
            "when initalized board state has an open tile",
        )

    def test_open_tile(self):
        pass

    def test_flag_tile(self):
        pass

    def test_count_surrounding_bombs(self):
        pass


class TestOpenTile(unittest.TestCase):

    def test_open_tile_flagged(self):
        m_indices = [(0, 0)]
        board = init_test_board(10, m_indices)
        f_indices = [(0, 0)]
        board_state = init_test_board_state(10, f_indices, [])
        actual_val = minesweeper.open_tile(board_state, board, 0, 0)
        expected_val = board_state
        self.assertTrue((actual_val == expected_val).all(),
                        f"expected {expected_val} but got {actual_val}")

    def test_open_tile_bomb(self):
        m_indices = [(5, 5)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [])
        actual_val = minesweeper.open_tile(board_state, board, 5, 5)
        expected_val = board_state.copy()
        self.assertTrue((actual_val == expected_val).all(),
                        f"expected {expected_val} but got {actual_val}")

    def test_open_tile_bomb_nearby(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [])
        actual_val = minesweeper.open_tile(board_state, board, 5, 5)
        expected_val = board_state.copy()
        expected_val[5][5] = 1
        self.assertTrue((actual_val == expected_val).all(),
                        f"expected {expected_val} but got {actual_val}")

    def test_open_tile_no_bombs(self):
        board = init_test_board(10, [])
        board_state = init_test_board_state(10, [], [])
        actual_val = minesweeper.open_tile(board_state, board, 5, 5)
        expected_val = np.zeros((10, 10))
        self.assertTrue((actual_val == expected_val).all(),
                        f"expected {expected_val} but got {actual_val}")


class TestFlagTile(unittest.TestCase):
    def test_flag_tile(self):
        pass


class TestCountSurroundingBombs(unittest.TestCase):
    def test_count_surrounding_bombs_simple(self):
        m_indices = [(0, 0), (6, 6), (4, 5), (5, 6)]
        board = init_test_board(10, m_indices)
        actual_val = minesweeper.count_surrounding_bombs(board, 5, 5)
        expected_val = 3
        self.assertEqual(
            actual_val, expected_val, f"expected {expected_val} but got {actual_val}"
        )

    def test_count_surrounding_bombs_none(self):
        m_indices = [(0, 0), (6, 6), (4, 5), (5, 6)]
        board = init_test_board(10, m_indices)
        actual_val2 = minesweeper.count_surrounding_bombs(board, 2, 2)
        expected_val2 = 0
        self.assertEqual(
            actual_val2,
            expected_val2,
            f"expected {expected_val2} but got {actual_val2}",
        )

    def test_count_surrounding_bombs_edge(self):
        m_indices = [(0, 0), (6, 6), (4, 5), (5, 6)]
        board = init_test_board(10, m_indices)
        actual_val3 = minesweeper.count_surrounding_bombs(board, 1, 0)
        expected_val3 = 1
        self.assertEqual(
            actual_val3,
            expected_val3,
            f"expected {expected_val3} but got {actual_val3}",
        )


class TestGameLost(unittest.TestCase):
    def test_game_lost(self):
        pass


class TestGameWon(unittest.TestCase):
    def game_game_won(self):
        pass


class TestAIHeuristicLogic(unittest.TestCase):
    def test_ai_heuristic_logic(self):
        pass


unittest.main()

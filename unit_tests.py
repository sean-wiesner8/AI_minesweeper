import heuristic_model
import minesweeper
import numpy as np
import unittest
from sympy import *
from collections import deque


def init_test_board(size, m_indices):
    init_board = np.zeros((size, size))
    for i, j in m_indices:
        init_board[i][j] = 1
    return init_board


# the change in tile for each of the 8 surrounding tiles
coordinates = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}


def init_test_board_state(size, f_indices, o_indices, board):
    board_state = minesweeper.init_board_state(size)
    for i, j in f_indices:
        board_state[i][j] = -2
    for i, j in o_indices:
        mine_count = 0
        for r, c in coordinates:
            if (
                i + r >= 0
                and j + c >= 0
                and i + r < len(board)
                and j + c < len(board[0])
                and board[i + r][j + c] == 1
            ):
                mine_count += 1
        board_state[i][j] = mine_count
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


class TestOpenTile(unittest.TestCase):
    def test_open_tile_flagged(self):
        m_indices = [(0, 0)]
        board = init_test_board(10, m_indices)
        f_indices = [(0, 0)]
        board_state = init_test_board_state(10, f_indices, [], board)
        actual_val = minesweeper.open_tile(board_state, board, 0, 0)
        expected_val = board_state
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )

    def test_open_tile_bomb(self):
        m_indices = [(5, 5)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        actual_val = minesweeper.open_tile(board_state, board, 5, 5)
        expected_val = board_state.copy()
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )

    def test_open_tile_bomb_nearby(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        actual_val = minesweeper.open_tile(board_state, board, 5, 5)
        expected_val = board_state.copy()
        expected_val[5][5] = 1
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )

    def test_open_tile_no_bombs(self):
        board = init_test_board(10, [])
        board_state = init_test_board_state(10, [], [], board)
        actual_val = minesweeper.open_tile(board_state, board, 5, 5)
        expected_val = np.zeros((10, 10))
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )


class TestFlagTile(unittest.TestCase):
    def test_flag_tile(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        actual_val = minesweeper.flag_tile(board_state, 4, 4)
        expected_val = init_test_board_state(10, m_indices, [], board)
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )

    def test_unflag_tile(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        flag_state = minesweeper.flag_tile(board_state, 4, 4)
        actual_val = minesweeper.flag_tile(board_state, 4, 4)
        expected_val = board_state
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )


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
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        lost_board_state = minesweeper.open_tile(board_state, board, 4, 4)
        actual_val = minesweeper.game_lost(board, lost_board_state)
        expected_val = True
        self.assertEqual(
            actual_val,
            expected_val,
            f"expected {expected_val} but got {actual_val}",
        )

    def test_game_not_lost(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        not_lost_board_state = minesweeper.open_tile(board_state, board, 4, 5)
        actual_val = minesweeper.game_lost(board, not_lost_board_state)
        expected_val = False
        self.assertEqual(
            actual_val,
            expected_val,
            f"expected {expected_val} but got {actual_val}",
        )


class TestGameWon(unittest.TestCase):
    def game_game_won(self):
        m_indices = [(0, 0)]
        board = init_test_board(2, m_indices)
        board_state = init_test_board_state(1, [], [(0, 1), (1, 0), (1, 1)], board)
        actual_val = minesweeper.game_won(board_state, 1)
        expected_val = True
        self.assertEqual(
            actual_val,
            expected_val,
            f"expected {expected_val} but got {actual_val}",
        )

    def game_not_won(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        actual_val = minesweeper.game_won(board_state, 1)
        expected_val = False
        self.assertEqual(
            actual_val,
            expected_val,
            f"expected {expected_val} but got {actual_val}",
        )


class TestAIHeuristicLogic(unittest.TestCase):
    def test_to_matrix_all_unopened(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        actual_val = heuristic_model.to_matrix(board_state)
        tile_count = len(board_state) ** 2
        expected_val = np.zeros((tile_count, tile_count + 1))
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )

    def test_to_matrix_one_opened(self):
        m_indices = [(0, 0)]
        board = init_test_board(2, m_indices)
        board_state = init_test_board_state(2, [], [], board)
        board_state = minesweeper.open_tile(board_state, board, 1, 1)
        actual_val = heuristic_model.to_matrix(board_state)
        tile_count = len(board_state) ** 2
        expected_val = np.zeros((tile_count, tile_count + 1))
        expected_val[3][0] = 1
        expected_val[3][1] = 1
        expected_val[3][2] = 1
        expected_val[3][4] = 1
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )

    def test_to_matrix_all_but_1(self):
        m_indices = [(0, 0)]
        board = init_test_board(2, m_indices)
        board_state = init_test_board_state(2, [], [], board)
        board_state = minesweeper.open_tile(board_state, board, 0, 1)
        board_state = minesweeper.open_tile(board_state, board, 1, 0)
        board_state = minesweeper.open_tile(board_state, board, 1, 1)
        actual_val = heuristic_model.to_matrix(board_state)
        tile_count = len(board_state) ** 2
        expected_val = np.zeros((tile_count, tile_count + 1))
        expected_val[1][0] = 1
        expected_val[2][0] = 1
        expected_val[3][0] = 1
        expected_val[1][4] = 1
        expected_val[2][4] = 1
        expected_val[3][4] = 1
        self.assertTrue(
            (actual_val == expected_val).all(),
            f"expected {expected_val} but got {actual_val}",
        )

    def test_analyze_matrix_all_unopened(self):
        m_indices = [(0, 0)]
        board = init_test_board(2, m_indices)
        board_state = init_test_board_state(2, [], [], board)
        board_state = minesweeper.open_tile(board_state, board, 0, 1)
        board_state = minesweeper.open_tile(board_state, board, 1, 0)
        board_state = minesweeper.open_tile(board_state, board, 1, 1)
        actual_val = heuristic_model.to_matrix(board_state)
        board_rep = Matrix(board_rep)
        board_rep.rref()
        actual_val = heuristic_model.analyze_matrix(board_rep, board_state)
        expected_val = deque()
        expected_val.append("flag", 0, 0)
        while actual_val and expected_val:
            self.assertEqual(
                actual_val.popleft(),
                expected_val.popleft(),
                f"expected {expected_val} but got {actual_val}",
            )

    def test_analyze_matrix_all_unopened(self):
        m_indices = [(4, 4)]
        board = init_test_board(10, m_indices)
        board_state = init_test_board_state(10, [], [], board)
        board_rep = heuristic_model.to_matrix(board_state)
        board_rep = Matrix(board_rep)
        board_rep.rref()
        actual_val = heuristic_model.analyze_matrix(board_rep, board_state)
        expected_val = deque()
        while actual_val and expected_val:
            self.assertEqual(
                actual_val.popleft(),
                expected_val.popleft(),
                f"expected {expected_val} but got {actual_val}",
            )


unittest.main()

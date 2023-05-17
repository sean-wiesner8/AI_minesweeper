import numpy as np


class GameBoard:


    """
    GameBoard class represents the game board for the Minesweeper game.
    """


    def __init__(self, size=22, n_mines=99):
        """
        Initializes a MineSweeper instance.

        Parameters:
        - size (int): The size of the game board (default: 22).
        - n_mines (int): The number of mines to be placed on the game board (default: 99).
        """

        self.size = 22
        self.n_mines = n_mines

        self.mines_grid = np.empty([self.size, self.size])
        self.mines_grid.fill(0)

        self.neighbors_grid = np.empty([self.size, self.size])
        self.neighbors_grid.fill(0)

        self.board_state = np.empty([self.size, self.size])
        self.board_state[:] = np.nan
        
        self.is_init = False
        self.game_over = False
        self.victory = False


    def initialize(self, coordinates):
        """
        Initializes the game board by placing mines and setting up neighbors.

        Parameters:
        - coordinates (tuple): The coordinates of the first selected cell.
        """
        selected = coordinates[0] * self.size + coordinates[1]
        self.set_up_mines(selected)
        self.set_up_neighbors()
        self.is_init = True


    def set_up_mines(self, selected):
        """
        Sets up mines in the game board.

        Parameters:
        - selected (int): The selected cell.
        """
        availableCells = np.arange(self.size**2)
        offLimits = self.calculate_offLimits(selected)
        availableCells = np.setdiff1d(availableCells, offLimits)
        self.n_mines = min(self.n_mines, len(availableCells))
        minesFlattened = np.zeros([self.size**2])
        minesFlattened[np.random.choice(
            availableCells, self.n_mines, replace=False)] = 1
        self.mines_grid = minesFlattened.reshape([self.size, self.size])


    def calculate_offLimits(self, selected):
        """
        Calculates off limits cells in the game board.

        Parameters:
        - selected (int): The selected cell.
        """
        return np.array([
            selected - self.size - 1, selected - self.size, selected - self.size + 1,
            selected - 1, selected, selected + 1,
            selected + self.size - 1, selected + self.size, selected + self.size + 1
        ])


    def set_up_neighbors(self):
        """
        Sets up neighbors in the game board.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.neighbors_grid[i, j] = self.calculate_neighbors(i, j)


    def calculate_neighbors(self, i, j):
        """
        Calculates the number of neighbors for a given cell.

        Parameters:
        - i (int): The row of the cell.
        - j (int): The column of the cell.
        """
        nNeighbors = 0
        for k in range(-1, 2):
            if 0 <= i + k < self.size:
                for l in range(-1, 2):
                    if 0 <= j + l < self.size and (k != 0 or l != 0):
                        nNeighbors += self.mines_grid[i + k, j + l]
        return nNeighbors



    def clearEmptyCell(self, coordinates):
        """
        Recursive function to clear empty cells and reveal neighboring cells.

        Parameters:
        - coordinates (tuple): The coordinates of the cell to clear.
        """

        x, y = coordinates
        self.board_state[x, y] = self.neighbors_grid[x, y]

        if self.board_state[x, y] == 0:
            for i in range(-1, 2):
                if 0 <= x + i < self.size:
                    for j in range(-1, 2):
                        if 0 <= y + j < self.size:
                            if np.isnan(self.board_state[x + i, y + j]):
                                self.clearEmptyCell((x + i, y + j))


    def select_cell(self, coordinates):
        """
        Handles the selection of a cell on the game board.

        Parameters:
        - coordinates (tuple): The coordinates of the selected cell.
        """

        if self.mines_grid[coordinates[0], coordinates[1]] > 0:
            self.game_over = True
            self.victory = False
        else:
            if not self.is_init:
                self.initialize(coordinates)
            self.clearEmptyCell(coordinates)
            if np.sum(np.isnan(self.board_state)) == self.n_mines:
                self.game_over = True
                self.victory = True

import numpy as np
from GameBoard import GameBoard
from keras.models import load_model

CNN = load_model("CNN.h5") #import default model (CNN)


class Trainer:
    def __init__(self, model = CNN):
        """
        Initializes the Mine Sweeper Trainer.

        Args:
            name (str): The name of the learner.
            model: The model used for learning.
        """
        self.model = model
        self.size = 22
        self.n_cells = self.size**2

    def train_model(self, samples_per_batch, total_batches, epochs_per_batch):
        """
        The main training function.

        Args:
            samples_per_batch (int): Number of samples in each batch.
            total_batches (int): Total number of batches.
            epochs_per_batch (int): Number of training epochs for each batch.
            
        This function runs the training process over the specified number of batches, generates training data for each batch,
        trains the model, and saves the model every 10th batch.
        """
        X, X2, y = self._initialize_samples(samples_per_batch)
        for batch in range(total_batches):
            X, X2, y, games_played, cells_revealed, games_won = self._play_games(
                samples_per_batch, X, X2, y)
            self._print_training_info(
                batch, games_played, cells_revealed, games_won)
            self.model.fit([X, X2], y, batch_size=samples_per_batch,
                           epochs=epochs_per_batch)
            if batch % 10 == 0:
                self.model.save("CNN.h5")


    def _initialize_samples(self, samples_per_batch):
        X = np.zeros((samples_per_batch, 11, self.size, self.size))
        X2 = np.zeros((samples_per_batch, 1, self.size, self.size))
        y = np.zeros((samples_per_batch, 1, self.size, self.size))
        return X, X2, y


    def _play_games(self, samples_per_batch, X, X2, y):
        cells_revealed, games_played, games_won, samples_taken = 0, 0, 0, 0
        while samples_taken < samples_per_batch:
            board = GameBoard()
            board.select_cell((self.size // 2, self.size // 2))
            X, X2, y, samples_taken = self._process_game(
                board, samples_per_batch, X, X2, y, samples_taken)
            if board.game_over:
                games_played += 1
                cells_revealed += self.n_cells - np.sum(np.isnan(board.board_state))
                if board.victory:
                    games_won += 1
        return X, X2, y, games_played, cells_revealed, games_won


    def _process_game(self, board, samples_per_batch, X, X2, y, samples_taken):
        while not (board.game_over or samples_taken == samples_per_batch):
            X_now, X2_now = self._extract_features(board.board_state)
            X[samples_taken], X2[samples_taken] = X_now, X2_now
            out, selected1, selected2 = self._predict_and_select_cell(
                X_now, X2_now)
            board.select_cell((selected1, selected2))
            y[samples_taken] = self._get_truth(out, board, selected1, selected2)
            samples_taken += 1
        return X, X2, y, samples_taken


    def _extract_features(self, board_state):
        X_now = self.extract_predictors(board_state)
        X2_now = np.array([np.where(X_now[0] == 0, 1, 0)])
        return X_now, X2_now


    def _predict_and_select_cell(self, X_now, X2_now):
        out = self.model.predict([np.array([X_now]), np.array([X2_now])])
        ordered_probs = np.argsort(out[0][0] + X_now[0], axis=None)
        selected = ordered_probs[0]
        selected1 = int(selected / self.size)
        selected2 = selected % self.size
        return out, selected1, selected2


    def _get_truth(self, out, board, selected1, selected2):
        truth = out
        truth[0, 0, selected1, selected2] = board.mines_grid[selected1, selected2]
        return truth[0]


    def _print_training_info(self, batch, games_played, cells_revealed, games_won):
        if games_played > 0:
            mean_cells_revealed = float(cells_revealed) / games_played
            prop_games_won = float(games_won) / games_played
            print(f"Batch {batch}:\n"
                  f"Games played: {games_played}\n"
                  f"Mean cells revealed: {mean_cells_revealed}\n"
                  f"Proportion of games won: {prop_games_won}\n")

    def extract_predictors(self, state):
        """
        Retrieves predictors from the board state.

        Args:
            state: The board state.

        Returns:
            out: The predictors extracted from the board state.
        """
        out = np.zeros((11, self.size, self.size))
        out[0] = np.where(np.isnan(state), 0, 1)
        out[1] = np.ones((self.size, self.size))
        out[2:11] = np.where(np.broadcast_to(
            state, (9, self.size, self.size)) == np.arange(9)[:, None, None], 1, 0)
        return out



    def test(self, n_games):
        """
        Tests the model by playing MineSweeper games.

        Args:
            n_games (int): Number of games to play.
        """
        cells_revealed = 0
        games_won = 0
        for i in range(n_games):
            if (i % 10) == 0:
                print("Playing game {}...".format(i + 1))
            cells, won = self.play_game()
            cells_revealed += cells
            games_won += won

        mean_cells_revealed = float(cells_revealed) / n_games
        prop_games_won = float(games_won) / n_games

        print("Proportion of games won: {}".format(prop_games_won))
        print("Mean cells revealed: {}".format(mean_cells_revealed))


    def play_game(self):
        """
        Plays a single game of MineSweeper.

        Returns:
            cells_revealed (int): Number of cells revealed during the game.
            game_won (int): Indicator whether the game was won (1) or not (0).
        """
        board = GameBoard()
        board.select_cell((int(self.size / 2), int(self.size / 2)))

        cells_revealed = 0
        games_won = 0

        while not board.game_over:
            X_now = self.extract_predictors(board.board_state)
            X2_now = np.array([np.where(X_now[0] == 0, 1, 0)])
            out = self.model.predict([np.array([X_now]), np.array([X2_now])])
            ordered_probs = np.argsort(out[0][0] + X_now[0], axis=None)
            selected = ordered_probs[0]
            selected1 = int(selected / self.size)
            selected2 = selected % self.size
            board.select_cell((selected1, selected2))

        cells_revealed += self.n_cells - np.sum(np.isnan(board.board_state))
        if board.victory:
            games_won += 1

        return cells_revealed, games_won

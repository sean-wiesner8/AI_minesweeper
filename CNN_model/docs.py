import numpy as np
from GameBoard import MineSweeper
from keras.models import load_model

CNN = load_model("CNN.h5")  # import default model (CNN)


class MineSweeperLearner:
    def __init__(self, name='CNN', model=CNN):
        """
        Initializes the MineSweeperLearner.

        Args:
            name (str): The name of the learner.
            model: The model used for learning.
        """
        self.name = name
        self.model = model
        self.size = 22

    def extract_predictors(self, state):
        """
        Extracts predictors from the game state.

        Args:
            state: The game state.

        Returns:
            predictors: The predictors extracted from the game state.
        """
        is_nan_mask = np.isnan(state)
        state_mask = [state == i for i in range(9)]

        predictors = [is_nan_mask.astype(int), np.ones(
            (self.size, self.size))] + [mask.astype(int) for mask in state_mask]

        return np.stack(predictors)

    def train_model(self, samples_per_batch, total_batches, epochs_per_batch):
        """
        Train the MineSweeper model.

        Args:
            samples_per_batch (int): Number of samples in each batch.
            total_batches (int): Total number of batches.
            epochs_per_batch (int): Number of training epochs for each batch.
            
        This function runs the training process over the specified number of batches, generates training data for each batch,
        trains the model, and saves the model every 10th batch.
        """
        for batch in range(total_batches):
            X_train, X2_train, y_train, games, avg_cells_revealed, win_ratio = self.generate_training_data(
                samples_per_batch)

            self.print_training_stats(
                batch, games, avg_cells_revealed, win_ratio)

            self.model.fit([X_train, X2_train], y_train, batch_size=samples_per_batch,
                           epochs=epochs_per_batch)

            if (batch + 1) % 10 == 0:
                self.model.save(f"trainedModels/{self.name}.h5")

    def generate_training_data(self, n_samples):
        """
        Generates the training data for a batch.

        Args:
            n_samples (int): Number of samples per batch.
            
        This function initializes the training data arrays and the game stats, 
        then plays games and updates the game stats until enough samples have been gathered.
        """
        X = np.zeros((n_samples, 11, self.size, self.size))
        X2 = np.zeros((n_samples, 1, self.size, self.size))
        y = np.zeros((n_samples, 1, self.size, self.size))
        cells_revealed, games_played, games_won, samples_taken = 0, 0, 0, 0
        mean_cells_revealed, prop_games_won = 0, 0  # Initialize variables here

        while samples_taken < n_samples:
            game, samples_taken = self.play_game(
                samples_taken, n_samples, X, X2, y)
            if game.game_over:
                games_played, cells_revealed, games_won = self.update_game_stats(
                    game, games_played, cells_revealed, games_won)

        if games_played > 0:
            mean_cells_revealed = float(cells_revealed) / games_played
            prop_games_won = float(games_won) / games_played

        return X, X2, y, games_played, mean_cells_revealed, prop_games_won

    def play_game(self, samples_taken, n_samples, X, X2, y):
        """
        Plays a single game and gathers samples.

        Args:
            game (MineSweeper): The game to play.
            samples_taken (int): The number of samples taken so far.
            X (numpy array): The array for the predictor variables.
            X2 (numpy array): The array for the auxiliary predictor variables.
            y (numpy array): The array for the target variable.
            
        This function initializes a game, selects the initial cell, 
        and continues to take samples until the game is over or enough samples have been gathered.
        """
        game = MineSweeper()
        game.select_cell((self.size // 2, self.size // 2))

        while not (game.game_over or samples_taken == n_samples):
            X_now, X2_now, truth, selected1, selected2 = self.take_sample(game)
            X[samples_taken], X2[samples_taken], y[samples_taken] = X_now, X2_now, truth[0]
            game.select_cell((selected1, selected2))
            samples_taken += 1

        return game, samples_taken

    def take_sample(self, game):
        """
        Takes a single sample from the current game.

        Args:
            game (MineSweeper): The game to take a sample from.
            
        This function gets the current state of the game, predicts the probabilities of each cell being a mine, 
        selects the cell with the lowest probability, and adds the ground truth for the selected cell.
        """
        X_now = self.extract_predictors(game.state)
        X2_now = np.array([np.where(X_now[0] == 0, 1, 0)])
        out = self.model.predict([np.array([X_now]), np.array([X2_now])])
        ordered_probs = np.argsort(out[0][0] + X_now[0], axis=None)
        selected = ordered_probs[0]
        selected1 = int(selected / self.size)
        selected2 = selected % self.size
        truth = out
        truth[0, 0, selected1, selected2] = game.mines[selected1, selected2]

        return X_now, X2_now, truth, selected1, selected2

    def update_game_stats(self, game, games_played, cells_revealed, games_won):
        """
        Updates the stats after a game.

        Args:
            game (MineSweeper): The game that was played.
            games_played (int): The number of games played so far.
            cells_revealed (int): The number of cells revealed so far.
            games_won (int): The number of games won so far.
            
        This function increments the number of games played, updates the number of cells revealed, 
        and increments the number of games won if the game was a victory.
        """
        games_played += 1
        cells_revealed += (self.size**2) - np.sum(np.isnan(game.state))
        if game.victory:
            games_won += 1

        return games_played, cells_revealed, games_won

    def print_training_stats(self, batch_num, games_played, mean_cells_revealed, prop_games_won):
        print(f"Batch {batch_num}:\n"
              f"Games played: {games_played}\n"
              f"Mean cells revealed: {mean_cells_revealed}\n"
              f"Proportion of games won: {prop_games_won}\n")

    def test(self, n_games):
        """
        Tests the model by playing MineSweeper games.

        Args:
            n_games (int): Number of games to play.
        """
        cells_revealed = 0
        games_won = 0
        for _ in range(n_games):
            game = MineSweeper()
            game.select_cell((int(self.size / 2), int(self.size / 2)))
            while not game.game_over:
                X_now = self.extract_predictors(game.state)
                X2_now = np.array([np.where(X_now[0] == 0, 1, 0)])
                out = self.model.predict(
                    [np.array([X_now]), np.array([X2_now])])
                ordered_probs = np.argsort(out[0][0] + X_now[0], axis=None)
                selected = ordered_probs[0]
                selected1 = int(selected / self.size)
                selected2 = selected % self.size
                game.select_cell((selected1, selected2))
            cells_revealed += (self.size**2) - np.sum(np.isnan(game.state))
            if game.victory:
                games_won += 1
        mean_cells_revealed = float(cells_revealed) / n_games
        prop_games_won = float(games_won) / n_games
        print(f"The model won {prop_games_won} % of the games.")
        print(
            f"The model won {round(mean_cells_revealed / (self.size ** 2), 2)} % of the tiles.")

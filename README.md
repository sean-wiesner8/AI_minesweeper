# How to Best Approach Modeling Minesweeper

By: Sean Weisner (saw336), Diego Virtue (dtv25), Frank Zhou (fcz5)

Link to paper: https://docs.google.com/document/d/18SRsW-SpH7Gs73xyqAHALdgLe8Q-qOZ2oVjYi7hlL-0/edit?usp=sharing

This README.md serves as a guide for how to run our code. 

'''
Please run the following commands: <br>
pip install sympy <br>
pip install numpy <br>
pip install matplotlib <br>
pip install contextlib <br>
pip install unittest <br>
pip install torch <br>
pip install torchvision <br>
'''

To "build" a variation of the probabilistic model, `run minesweeper.py` and follow the instructions provided by the terminal.
We suggest running the following parameters for board size (n x n) and mine count (m) based on the following difficulties:
Beginner: n = 9, m = 10
Intermediate: n = 16, m = 40
Expert: n = 22, m = 99
Then specify if you want to use the Single-Point or Constraint Satisfaction alogirthm to run, and then specify if you want a random tile to open the tile with the lowest local probability given the need to make an uncertain move.  

To train a DQN: `run agent.py` in the `DeepQModel` directory. You can select the game board size by modifying the 'NUM_TILES' variable on line 17, and you can select the number of mines by modifying the 'NUM_MINES' variable on line 18. If you would like to change the number of game iterations that the model trains on, edit the 'num_episodes' variable on line 148 if you plan to train on your GPU, and edit the same variable on line 150 if you plan to train on your CPU. If you would like to save the model, change the name of the model on line 196 and run the code. Your model will be saved in the `DeepQModel` directory.

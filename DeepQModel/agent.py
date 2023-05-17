from collections import namedtuple, deque
from itertools import count
import random

import torch
import torch.optim as optim

import minesweeper
import DQN

#env = ENV_NAME

#use GPU instead of CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


#class to store periods of batches
class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
    
#Parameters
BATCH_SIZE = 64
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4
DENSE_CHANNELS = 512

#TODO 1: initialize environment, define state variables, neural networks, and optimizer.





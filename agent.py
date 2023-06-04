from collections import namedtuple, deque
from itertools import count
import random
import time
import gymnasium as gym
import matplotlib
import matplotlib.pyplot as plt
import math

import torch
import torch.optim as optim
import torch.nn as nn

import DQN_Env
import network

NUM_TILES = 22
NUM_MINES = 99
start_time = time.time()

env = DQN_Env.DQEnvironment(NUM_MINES, NUM_TILES)

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()

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
EPS_END = 1e-10
EPS_DECAY = 10000
TAU = 0.005
LR = 1e-4
DENSE_CHANNELS = 512

n_actions, n_observations = env.board_size, env.board_size
env.reset()

policy_net = network.DQN(n_observations ** 2, n_actions ** 2, n_observations ** 2).to(device)
target_net = network.DQN(n_observations ** 2, n_actions ** 2, n_observations ** 2).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)


steps_done = 0

#Code from https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        rand_list = []
        for r in range(env.board_size):
            for c in range(env.board_size):
                if env.board_state[r][c] == -1: rand_list.append(r * env.board_size + c)
        return torch.tensor([[random.choice(rand_list)]], device=device, dtype=torch.long)


episode_durations = []

def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)
    if is_ipython:
        if not show_result:
            display.display(plt.gcf())
            display.clear_output(wait=True)
        else:
            display.display(plt.gcf())

#Code from https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

if torch.cuda.is_available():
    num_episodes = 200
else:
    num_episodes = 200

most_opened = 0
for i_episode in range(num_episodes):
    if i_episode % 50 == 0: print(f"episode {i_episode}")
  
    env.reset()
    state = env.board_state.flatten('C')
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    for t in count():
        action = select_action(state)
        board_state, reward, done = env.step(action.item())
        board_state = board_state.flatten('C') #flatten input for model
        reward = torch.tensor([reward], device=device)
        
        if done:
            next_state = None
        else:
            next_state = torch.tensor(board_state, dtype=torch.float32, device=device).unsqueeze(0)

        memory.push(state, action, next_state, reward)
        state = next_state

        optimize_model()

        target_net_state_dict = target_net.state_dict()
        policy_net_state_dict = policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        target_net.load_state_dict(target_net_state_dict)

        if done:
            opened = 0
            for r in range(env.board_size):
                for c in range(env.board_size):
                    if env.board_state[r][c] in range(0, 9):
                        opened += 1
            print(opened)
            if opened > most_opened:
                most_opened = opened
                print(f"the new highest count is {most_opened}")
            episode_durations.append(t + 1)
            plot_durations()
            break
end_time = time.time()
print('Time took to train: ', end_time - start_time, ' seconds')
torch.save(policy_net, 'model2.pt')
print('Complete')
plot_durations(show_result=True)
plt.ioff()
plt.show()

# env.reset()
# opened_list = []
# num_data = 1
# for iter in range(num_data):
#     env.reset()
#     done = False
#     while not done:
#         input_val = env.board_state.flatten('C')
#         state = torch.tensor(input_val, dtype=torch.float32, device=device).unsqueeze(0)
#         action = policy_net(state).max(1)[1].view(1, 1)
#         board_state, reward, done = env.step(action.item())
#         action_row = action // env.board_size
#         action_col = action % env.board_size
#         if env.board[action_row][action_col] == 1:
#             opened = 0
#             for r in range(env.board_size):
#                 for c in range(env.board_size):
#                     if env.board_state[r][c] in range(0, 9):
#                         opened += 1
#             opened_list.append(opened)
#             done = True
            
# print('average number of mines opened', sum(opened_list) / num_data)
            
        









import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    
    def __init__(self, batch_size, num_actions, num_dense):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(batch_size, num_dense)
        self.layer2 = nn.Linear(num_dense, num_dense)
        self.layer3 = nn.Linear(num_dense, num_actions)
        

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return F.softmax(self.layer2(x), 0)
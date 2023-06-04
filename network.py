import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    
    def __init__(self, num_tiles, num_actions, num_dense):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(num_tiles, num_dense)
        self.layer2 = nn.Linear(num_dense, num_dense)
        self.layer3 = nn.Linear(num_dense, num_actions)
        

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return F.softmax(x, 0)
    

class DQN2(nn.Module):

    def __init__(self, in_channels, conv_units, num_actions):
        super(DQN2, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, conv_units, kernel_size=3, stride=1)
        self.fc = nn.Linear(conv_units * 22 * 22, num_actions)

    def forward(self, x):
        batch_size = x.size(dim=0)
        x = self.conv1(x)
        x = F.relu(x)
        x = x.view(batch_size, -1)
        x = self.fc(x)
        return F.softmax(x)

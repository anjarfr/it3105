import torch
import torch.nn as nn
from .critic import Critic
import numpy as np

torch.manual_seed(42)

class TorchCritic(Critic):

    def __init__(self, cfg, init_state):
        super(TorchCritic, self).__init__(cfg)
        self.model = TorchNet(cfg, init_state)

    def calculate_TD_error(self, state, succ_state, reward):
        """  """
        state = self.generate_state(state)
        succ_state = self.generate_state(succ_state)

        value_function_state = self.model.forward(state)
        value_function_succ_state = self.model.forward(succ_state)

        TD_error = reward + self.discount_factor * value_function_succ_state - value_function_state

        return TD_error[0].item()

    def reset_eligibility(self):
        for params in self.model.parameters():
            self.model.eligibility.append(torch.zeros(params.shape))

    def generate_state(self, state):
        """ Creates a tensor of state """
        listed_state = []
        for c in state:
            listed_state.append(int(c))
        tensor = torch.tensor(listed_state, dtype=torch.float32)
        return tensor

    def update_value_function(self, state, TD_error, reward=0, succ_state=None):
        state = self.generate_state(state)
        succ_state = self.generate_state(succ_state)

        prediction = self.model(state)
        target = reward + self.discount_factor * self.model(succ_state)

        self.model.update(prediction, target)


class TorchNet(nn.Module):

    def __init__(self, cfg, init_state):
        super(TorchNet, self).__init__()

        self.loss_func = nn.MSELoss()

        self.dimensions = cfg["critic"]["dimensions"]
        self.learning_rate = cfg["critic"]["learning_rate"]
        self.eligibility_decay = cfg["critic"]["eligibility_decay"]
        self.discount_factor = cfg["critic"]["discount_factor"]

        self.eligibility = []

        layers = []

        layers.append(nn.Linear(len(init_state), self.dimensions[0]))
        for i in range(len(self.dimensions) - 1):
            layers.append(nn.Linear(self.dimensions[i], self.dimensions[i+1]))
        self.layers = nn.ModuleList(layers)

    def update(self, prediction, target):
        loss = self.loss_func(prediction, target)
        self.zero_grad()
        loss.backward(retain_graph=True)

        for i, params in enumerate(self.parameters()):
            self.eligibility[i] = self.discount_factor * self.eligibility_decay * self.eligibility[i] + params.grad.data
            params.data.add_(self.learning_rate * (target - prediction) * self.eligibility[i])

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = torch.tanh(layer(x))
        x = self.layers[-1](x)
        return x

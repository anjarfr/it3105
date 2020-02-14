from keras.layers import *
from keras import Model

class Critic:
    """
    Receive SARSA from player
    Calculate TD error
    Update value function
    Send TD error to actor
    """

    def __init__(self, cfg):
        self.value_function = {}
        self.eligibility = {}

        # Constants
        self.learning_rate = cfg["critic"]["learning_rate"]
        self.eligibility_decay = cfg["critic"]["eligibility_decay"]
        self.discount_factor = cfg["critic"]["discount_factor"]

    def initialize_value_function(self, state: str):
        """
        Initialize V(s) to 0 if it does not already exist in V()
        """
        if not self.value_function.get(state):
            self.value_function[state] = 0

    def reset_eligibility(self):
        """
        Reset eligibilities to 0 for all s in self.eligibility
        """
        for key in self.eligibility:
            self.eligibility[key] = 0

    def set_current_eligibility(self, state):
        """
        Sets eligibility of the current state to 1
        """
        self.eligibility[state] = 1

    def update_eligibility(self, state):
        """
        Update eligibility with discount and decay
        """
        self.eligibility[state] = (
            self.discount_factor * self.eligibility_decay * self.eligibility[state]
        )

    def calculate_TD_error(self, state, succ_state, reward):
        """
        Calculates TD error
        """
        TD_error = (
            reward
            + self.discount_factor * self.value_function[succ_state]
            - self.value_function[state]
        )
        return TD_error

    def update_value_function(self, state, TD_error):
        """
        Update the value function for a state
        """
        self.value_function[state] += (
            self.learning_rate * TD_error * self.eligibility[state]
        )


class CriticNN(Critic):

    """
    Input as bit vector
    Target = r + discount_factor * V(s')
    Weight updates basis : dL/dw = -2 * TDerror * dV(s)/dw

    Conclusion:
    e_i = e_i + dV(s) / dw_i
    Weight update w_i = w_I + learning rate * TDerror * e_i
    """

    def __init__(self, cfg):
        super(CriticNN, self).__init__(cfg)

        self.dimensions = cfg["critic"]["dimensions"]  # List

    def build_model(self, state):

        # Gjør om state fra string til list sånn [0, 1, 1, 0] osv

        num_layers = len(self.dimensions)

        inp = Input(shape=state.shape[0])
        x = inp

        for i in range(num_layers):
            x = Dense(self.dimensions[i], activation='relu')(x)

        model = Model([inp, x])
        model.compile()

        # Connect to splitGD somehow, send in the model




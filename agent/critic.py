from tensorflow.keras.layers import *
from tensorflow.keras import Model, optimizers
import numpy as np
from agent.splitgd import SplitGD
import tensorflow as tf


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
        if self.value_function.get(state) is None:
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


class CriticNN(Critic, SplitGD):
    """
    Input as bit vector
    Target = r + discount_factor * V(s')
    Weight updates basis : dL/dw = -2 * TDerror * dV(s)/dw

    Conclusion:
    e_i = e_i + dV(s) / dw_i
    Weight update w_i = w_I + learning rate * TDerror * e_i
    """

    def __init__(self, cfg, init_state):
        self.dimensions = cfg["critic"]["dimensions"]  # List
        model = self.build_model(init_state)
        Critic.__init__(self, cfg)
        SplitGD.__init__(self, model)

        self.eligibility = []

    def generate_state(self, state):
        """ Creates a numpy array of state """
        listed_state = []
        for c in state:
            listed_state.append(int(c))
        array = np.array(listed_state)
        return array

    def build_model(self, init_state):
        """
        Build Keras model
        """
        state = self.generate_state(init_state)
        num_layers = len(self.dimensions)
        inp = Input(shape=state.shape)
        x = inp

        for i in range(num_layers):
            x = Dense(self.dimensions[i], activation='sigmoid')(x)

        sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        model = Model(inp, x)

        model.compile(loss='mean_squared_error', optimizer=sgd)
        model.summary()
        return model

    def calculate_TD_error(self, state, succ_state, reward):

        state = self.generate_state(state)
        state = np.expand_dims(state, axis=0)

        succ_state = self.generate_state(succ_state)
        succ_state = np.expand_dims(succ_state, axis=0)

        value_function_state = self.model.predict(state)[0, 0]
        value_function_succ_state = self.model.predict(succ_state)[0, 0]
        print(value_function_state)

        TD_error = min(1, (
                reward
                + self.discount_factor * value_function_succ_state
                - value_function_state)
        )
        print('TD error', TD_error)
        return TD_error

    def reset_eligibility(self):
        for weights in self.model.trainable_weights:
            self.eligibility.append(tf.zeros_like(weights))

    def modify_gradients(self, gradients, TD_error):
        for i in range(len(gradients)):
            self.eligibility[i] = tf.add(self.eligibility[i], gradients[i])
            gradients[i] = gradients[i] + self.learning_rate * TD_error[0] * self.eligibility[i]
        return gradients

    def update_value_function(self, state, TD_error):
        state = self.generate_state(state)
        state = np.expand_dims(state, axis=0)
        target = TD_error + self.model.predict(state)

        self.fit(state, target)

    def derivate_V(self, w_i):
        pass

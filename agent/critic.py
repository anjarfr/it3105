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
        """ Update eligibility with discount and decay """
        self.eligibility[state] = (
                self.discount_factor * self.eligibility_decay * self.eligibility[state]
        )

    def calculate_TD_error(self, state, succ_state, reward):
        """ Calculates TD error """
        TD_error = (
                reward
                + self.discount_factor * self.value_function[succ_state]
                - self.value_function[state]
        )
        return TD_error

    def update_value_function(self, state, TD_error, reward=0, succ_state=None):
        """
        Update the value function for a state
        """
        self.value_function[state] += (
                self.learning_rate * TD_error * self.eligibility[state]
        )

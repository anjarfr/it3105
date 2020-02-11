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

    def initialize_value_function(self, state):
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






    def get_value(self, state, action):
        return self.value_function.get((state, action))

    def update_value_function(self, action, reward, succ_state, succ_action, visited_SAP, eligibility):
        # TODO fix. Need to handle all successors, actions etc
        for state in visited_SAP:
            TD_error = self.calculate_TD_error(state, action, reward, succ_state, succ_action)
            self.value_function[state] += self.learning_rate * TD_error * eligibility[state]

    def calculate_TD_error(self, state, action, reward, succ_state, succ_action):
        TD_error = reward + self.discount_factor * self.get_value(succ_state, succ_action) - self.get_value(state, action)
        return TD_error

    def update_eligibility(self, curr_state, visited_SAP, eligibility):
        for state in visited_SAP:
            if state == curr_state:
                eligibility[state] = 1  # To avoid accumulating trace
            else:
                eligibility[state] = self.discount_factor * self.eligibility_decay * eligibility[state]

    def get_TD_error(self, state, action, reward, succ_state, succ_action):
        TD_error = self.calculate_TD_error(state, action, reward, succ_state, succ_action)
        return TD_error

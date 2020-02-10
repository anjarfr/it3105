class Critic:
    """
    Receive SARSA from player
    Calculate TD error
    Update value function
    Send TD error to actor
    """

    def __init__(self, init_state, cfg):
        self.value_function = {}
        self.init_state = init_state
        self.eligibility = {}
        self.visited_SAP = []

        self.current_state = self.init_state
        self.current_action = None
        self.reward = None
        self.succ_state = None
        self.succ_action = None
        self.TD_error = None

        # Constants
        self.learning_rate = cfg["critic"]["learning_rate"]
        self.eligibility_decay = cfg["critic"]["eligibility_decay"]
        self.discount_factor = cfg["critic"]["discount_factor"]

    def initialize_value_function(self):
        if not self.value_function.get((self.current_state, self.current_action)):
            self.value_function[(self.current_state, self.current_action)] = 0

    def update_value_function(self):
        for state in self.visited_SAP:
            self.value_function[state] += self.learning_rate * self.TD_error() * self.eligibility[state]

    def get_value(self, state, action):
        return self.value_function.get((state, action))

    def update_TD_error(self):
        self.TD_error = self.reward + self.discount_factor * self.get_value(self.succ_state, self.succ_action) \
                        - self.get_value(self.current_state, self.current_action)

    def update_eligibility(self):
        for state in self.visited_SAP:
            if state == self.current_state:
                self.eligibility[state] = 1  # To avoid accumulating trace
            else:
                self.eligibility[state] = self.discount_factor * self.eligibility_decay * self.eligibility[state]

    def get_input(self, state, action, reward, succ_state):
        self.current_state = state
        self.current_action = action
        self.reward = reward
        self.succ_state = succ_state
        self.succ_action = None  # TODO Find best possible action (ask actor? Hmm, doesnt seem right)
        self.visited_SAP.append((self.current_state, self.current_action))

        self.update_TD_error()
        self.update_value_function()
        self.update_eligibility()

        return self.TD_error

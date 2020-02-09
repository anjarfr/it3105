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
        self.learning_rate = cfg["critic"]["learning_rate"]
        self.eligibility_decay = cfg["critic"]["eligibility_decay"]
        self.discount_factor = cfg["critic"]["discount_factor"]

    def initialize_value_function(self, state, action):
        if not self.value_function.get((state, action)):
            self.value_function[(state, action)] = 0

    def update_value_function(self, state):
        pass

    def get_value(self, state, action):
        return self.value_function.get((state, action))

    def calculate_TD_error(self, state, action,  reward, succ_state, succ_action):
        TD_error = reward + self.get_value(succ_state, succ_action)


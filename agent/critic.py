class Critic:
    """
    Receive SARSA from player
    Calculate TD error
    Update value function
    Send TD error to actor
    """

    def __init__(self, cfg):
        self.value_function = {}

    def update_value_function(self, state, action, reward, succ_state):
        pass

    def calculate_TD_error(self, state, action,  reward, succ_state):
        pass

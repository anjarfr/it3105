class Actor:

    """
    Get current state and legal actions from player
    Decide action
    Update policy based on TD error
    """

    def __init__(self, init_state, cfg):
        self.policy = {}
        self.eligibility = {}

    def choose_action(self, state, actions):
        """
        Return chosen action
        """
        chosen_action = max(self.policy.get(state))
        return chosen_action

    def update_eligibility(self, state, action):
        self.eligibility[(state, action)] = 1

    def produce_initial_state(self):
        pass

    def game_is_over(self):
        pass


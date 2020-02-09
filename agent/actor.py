class Actor:

    """
    Get current state and legal actions from player
    Decide action
    Update policy based on TD error
    """

    def __init__(self, cfg):
        self.policy = {}

    def choose_action(self, state, actions):
        """
        Return state number (a1, a2, a3 etc)
        """
        pass

    def produce_initial_state(self):
        pass

    def game_is_over(self):
        pass

    def perform_action(self):
        pass

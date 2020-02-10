import random


class Actor:

    """
    Get current state and legal actions from player
    Decide action
    Update policy based on TD error
    """

    def __init__(self, cfg):
        self.policy = {}
        self.alpha = cfg['actor']['learning_rate']
        self.delta = cfg['actor']['eligibility_decay']
        self.gamma = cfg['actor']['discount_factor']
        self.epsilon = cfg['actor']['init_epsilon']
        self.epsilon_decay = cfg['actor']['epsilon_decay_rate']

    def produce_initial_state(self, init_state, init_actions):
        """ Initializes policy of inital state """
        for action in init_actions:
            self.policy[init_state, action] = 0

    def choose_action(self, state, actions):
        """
        Epsilon Greepy Policy for choosing action
        Choose the best possible action with a probability 1-e,
        and a random action with probability e
        """

        greedy_number = random.uniform(0, 1)

        if greedy_number >= self.e:
            best = 0
            for action in actions:
                if self.policy[state, action] > best:
                    best = self.policy[state, action]
                    chosen_action = action
        else:
            random_index = random.randint(0, len(actions))
            chosen_action = actions[random_index]

        return best

    def update_policy(
        self, state: object, action: tuple, td_error: float, eligibility: float
    ):
        """ Updates the policy for a given state and action based on the TD error
        computed by the Critic """

        try:
            self.policy[state, action] += self.a * self.d * eligibility
        except:
            self.policy[state, action] = self.a * self.d * eligibility


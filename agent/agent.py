class Agent:

    def __init__(self):
        self.actor = Actor()
        self.critic = Critic()
        self.e_s = {}

    def TD_learning(self):
        pass
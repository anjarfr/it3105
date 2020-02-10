from agent.actor import Actor
from agent.critic import Critic

class Agent:
    def __init__(self, cfg):
        self.actor = Actor(cfg)
        self.critic = Critic(cfg)
        self.e_s = {}

    def TD_learning(self, game):
        while not game.is_finished():
            state = game.board
            action = self.actor.choose_action(state, self.game.get_all_legal_actions())
            succ_state, reward = game.perform_action(action)
            self.critic.update_value_function(state, action, reward, succ_state)

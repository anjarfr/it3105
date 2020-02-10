from agent.actor import Actor
from agent.critic import Critic

class Agent:
    def __init__(self, cfg):
        self.actor = Actor(cfg)
        self.critic = Critic(cfg)
        self.eligibility = {}
        self.visited_SAP = []

    def TD_learning(self, game):
        while not game.is_finished():
            state = game.board
            action = self.actor.choose_action(state, game.get_all_legal_actions())
            succ_state, reward = game.perform_action(action)
            succ_action = self.actor.choose_action(state, game.get_all_legal_actions())
            TD_error = self.critic.get_TD_error(state, action, reward, succ_state, succ_action, self.visited_SAP,
                                                self.eligibility)

            self.critic.update_value_function(action, reward, succ_state, succ_action, self.visited_SAP,
                                              self.eligibility)
            self.critic.update_eligibility(state, self.visited_SAP, self.eligibility)

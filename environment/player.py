import yaml
from environment.game import Peg, Hex
from agent.actor import Actor
from agent.critic import Critic

with open("../config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

class Player:
    """
    Player is responsible for communication between environment and agent
    Initialize game, actor and critic
    Send state and legal actions to actor
    Get action from actor
    Perform action on environment
    Send resulting state and reward to critic
    """

    def __init__(self):
        self.game = self.initialize_game()
        self.actor = Actor(cfg)
        self.critic = Critic(cfg)
        self.episodes = cfg['RL_system']['episodes']
        self.visited_SAP = []

    def initialize_game(self):
        game_type = cfg["game"]["type"]
        if game_type == "Peg":
            game = Peg()
        if game_type == "Hex":
            game = Hex()
        return game

    def play_game(self):

        state = self.game.board
        possible_actions = self.game.get_all_legal_actions()

        self.critic.initialize_value_function(state)
        self.actor.initialize_policy(state, possible_actions)

        for i in range(self.episodes):
            self.critic.reset_eligibility()
            self.actor.reset_eligibility()

            while not self.game.is_finished():
                action = self.actor.choose_action(state, possible_actions)
                self.game.perform_action(action)


                self.visited_SAP.append((state, action))
                succ_state, reward = self.game.perform_action(action)
                succ_action = self.actor.choose_action(state, self.game.get_all_legal_actions())
                TD_error = self.critic.get_TD_error(state, action, reward, succ_state, succ_action)
                self.critic.update_value_function(action, reward, succ_state, succ_action, self.visited_SAP,
                                                  self.eligibility)
                self.critic.update_eligibility(state, self.visited_SAP, self.eligibility)


    def map_actions(self, actions):
        """
        Maps action from dictionary to list of tuples
        """
        listed_actions = []
        for key, values in actions:
            for value in values:
                listed_actions.append((key, value))
        return listed_actions

def main():
    pass

if __name__ == "__main__":
    main()



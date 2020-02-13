import yaml
from environment.game import Peg, Hex
from agent.actor import Actor
from agent.critic import Critic

with open("config.yml", "r") as ymlfile:
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
        self.episodes = cfg["RL_system"]["episodes"]
        self.visited_SAP = []

    def initialize_game(self):
        game_type = cfg["game"]["type"]
        if game_type == "Peg":
            game = Peg()
        if game_type == "Hex":
            game = Hex()
        return game

    def play_game(self):

        init_state = self.game.board
        possible_actions = self.game.get_all_legal_actions()

        self.critic.initialize_value_function(init_state)
        self.actor.initialize_policy(init_state, possible_actions)

        init_action = self.actor.choose_action(init_state, possible_actions)

        for i in range(self.episodes):
            state = init_state
            action = init_action

            self.critic.reset_eligibility()
            self.actor.reset_eligibilities()
            self.visited_SAP = []

            while not self.game.is_finished():

                self.critic.initialize_value_function(state)
                self.actor.initialize_policy(state, action)
                self.visited_SAP.append((state, action))

                succ_state, reward = self.game.perform_action(action)
                possible_succ_actions = self.actor.choose_action(
                    succ_state, self.game.get_all_legal_actions()
                )
                succ_action = self.actor.choose_action(
                    succ_state, possible_succ_actions
                )

                self.actor.set_current_eligibility(state, action)

                TD_error = self.critic.calculate_TD_error(state, succ_state, reward)
                self.critic.set_current_eligibility(state)

                for SAP in self.visited_SAP:
                    state = SAP[0]
                    action = SAP[1]

                    self.critic.update_value_function(state, TD_error)
                    self.critic.update_eligibility(state)

                    self.actor.update_policy(state, action, TD_error)
                    self.actor.update_eligibility(state, action)

                state = succ_state
                action = succ_action

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
    player = Player()
    player.play_game()


if __name__ == "__main__":
    main()


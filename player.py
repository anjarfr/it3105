import yaml
from environment.game import Peg, Hex
from agent.actor import Actor
from agent.critic import Critic
from environment.visualizer import Visualizer

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
        self.SAP_history = []
        self.visualizer = Visualizer(
            self.game.board, self.game.size, self.game.shape, cfg["display"]
        )

    def initialize_game(self):
        game_type = cfg["game"]["type"]
        if game_type == "Peg":
            game = Peg()
        if game_type == "Hex":
            game = Hex()
        return game

    def play_game(self):

        if cfg["display"]["frequency"] != 0:
            self.visualizer.fill_nodes(self.game.board.get_filled_cells())

        for i in range(self.episodes):
            """ New game """

            self.game = self.initialize_game()
            init_state = self.game.board.generate_state()  # String with state

            possible_actions = (
                self.game.get_all_legal_actions()
            )  # List of actions [(from), (to)]

            self.critic.initialize_value_function(
                init_state
            )  # Creares dictionary {string: value}
            self.actor.initialize_policy(
                init_state, possible_actions
            )  # Creates dictionary {string: tuple of tuple}

            init_action = self.actor.choose_action(
                init_state, possible_actions
            )  # Tuple of tuple

            state = init_state  # String
            action = init_action  # Tuple of tuple

            """ Reset all elegibilities to 0 """
            self.critic.reset_eligibility()
            self.actor.reset_eligibilities()
            self.SAP_history = []

            self.game.terminal_print()

            while not self.game.is_finished():

                """ Play game until termination """
                self.critic.initialize_value_function(
                    state
                )  # Initializes all new states to 0 at the start of an episode

                """ Do action a from state s to s', and receive reward r """
                reward = self.game.perform_action(action)  # Int
                succ_state = self.game.board.generate_state()  # String

                """ Add performed action to SAP history"""
                self.SAP_history.append((state, action))

                """ Dictate a' from the current policy for s' """
                possible_succ_actions = self.game.get_all_legal_actions()

                if len(possible_succ_actions) > 0:
                    succ_action = self.actor.choose_action(
                        succ_state, possible_succ_actions
                    )  # tuple of tuple

                    """ Dynamically update value function and policy as new """
                    self.critic.initialize_value_function(succ_state)
                    self.actor.initialize_policy(succ_state, possible_succ_actions)

                    """ Set eligibility of a and s to 1 """
                    self.actor.set_current_eligibility(state, action)

                    """ Compute TD error """
                    TD_error = self.critic.calculate_TD_error(state, succ_state, reward)

                    """ Set current state eligibility to 1 """
                    self.critic.set_current_eligibility(state)

                    for SAP in self.SAP_history:
                        state = SAP[0]
                        action = SAP[1]

                        self.critic.update_value_function(state, TD_error)
                        self.critic.update_eligibility(state)

                        self.actor.update_policy(state, action, TD_error)
                        self.actor.update_eligibility(state, action)

                    if cfg["display"]["frequency"] != 0:
                        if i % cfg["display"]["frequency"] == 0:
                            self.visualizer.fill_nodes(
                                self.game.board.get_filled_cells(), action[0], action[1]
                            )

                self.game.terminal_print()

                state = succ_state
                action = succ_action

            print(i, ": ", self.game.get_pegs())


def main():
    player = Player()
    player.play_game()


if __name__ == "__main__":
    main()

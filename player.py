import yaml
from environment.game import Peg, Hex
from agent.actor import Actor
from agent.critic import Critic, CriticNN
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
        self.table_critic = True
        self.critic = self.initialize_critic()
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

    def initialize_critic(self):
        critic_type = cfg["critic"]["type"]
        if critic_type == "table":
            critic = Critic(cfg)
        if critic_type == "NN":
            self.table_critic = False
            init_state = self.game.board.generate_state()
            critic = CriticNN(cfg, init_state)
        return critic

    def play_game(self):

        if cfg["display"]["frequency"] != 0:
            self.visualizer.fill_nodes(self.game.board.get_filled_cells())

        wins = 0

        """ New game """
        for i in range(self.episodes):

            """ Reset all elegibilities to 0 """
            self.critic.reset_eligibility()
            self.actor.reset_eligibilities()
            self.SAP_history = []

            """Initialize new game"""
            self.game = self.initialize_game()
            init_state = self.game.board.generate_state()  # String with state
            possible_actions = (self.game.get_all_legal_actions())  # List of actions [(from), (to)]
            self.actor.initialize_policy(init_state, possible_actions)  # Creates dictionary {string: tuple of tuple}
            init_action = self.actor.choose_action(init_state, possible_actions)  # Tuple of tuple

            if self.table_critic:
                self.critic.initialize_value_function(init_state)  # Creates dictionary {string: value}

            state = init_state  # String
            action = init_action  # Tuple of tuple

            """ Step counter for display frequency """
            step = 0

            """ Play game until termination """
            while not self.game.is_finished():

                """Initializes all new states to 0 at the start of an episode"""
                if self.table_critic:
                    self.critic.initialize_value_function(state)

                """ Do action a from state s to s', and receive reward r """
                reward = self.game.perform_action(action)  # Int
                succ_state = self.game.board.generate_state()  # String

                """ Add performed action to SAP history"""
                self.SAP_history.append((state, action))

                """ Dynamically update value function and policy as new """
                if self.table_critic:
                    self.critic.initialize_value_function(succ_state)

                """ Dictate a' from the current policy for s' """
                possible_succ_actions = self.game.get_all_legal_actions()

                succ_action = None
                if len(possible_succ_actions) > 0:
                    self.actor.initialize_policy(succ_state, possible_succ_actions)
                    succ_action = self.actor.choose_action(succ_state, possible_succ_actions)  # tuple of tuple

                """ Set eligibility of a and s to 1 """
                self.actor.set_current_eligibility(state, action)

                """ Compute TD error """
                TD_error = self.critic.calculate_TD_error(state, succ_state, reward)

                """ Set current state eligibility to 1 """
                if self.table_critic:
                    self.critic.set_current_eligibility(state)

                for SAP in self.SAP_history:
                    state = SAP[0]
                    action = SAP[1]

                    self.critic.update_value_function(state, TD_error)
                    if self.table_critic:
                        self.critic.update_eligibility(state)

                    self.actor.update_policy(state, action, TD_error)
                    self.actor.update_eligibility(state, action)

                if i in self.visualizer.diplay_range and cfg["display"]["frequency"] != 0:
                    if step % cfg["display"]["frequency"] == 0:
                        self.visualizer.fill_nodes(
                            self.game.board.get_filled_cells(), action[0], action[1]
                        )

                step += 1

                state = succ_state
                if succ_action:
                    action = succ_action

            pegs = self.game.get_pegs()
            if pegs == 1: wins += 1

            print(i, ": ", self.game.get_pegs(), ' pegs were left')

        print('Number of wins: ', wins)

    def visualize_target_policy(self):
        """
        After training, visualize a game played using the final policy
        """
        pass


def main():
    player = Player()
    player.play_game()
    # cNN = CriticNN(cfg)
    # cNN.build_model('01010101010101')

if __name__ == "__main__":
    main()

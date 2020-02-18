import matplotlib.pyplot as plt
import yaml

from agent.actor import Actor
from agent.critic import Critic
from agent.torch_critic import NeuralNetCritic
from environment.game import Peg, Hex
from environment.visualizer import Visualizer
import numpy as np

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
        self.display_last_game = cfg["display"]["display_last_game"]
        self.remaining_pegs = []
        self.iterations = []
        self.epsilon_greedy = True

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
        if critic_type == "nn" or critic_type == "NN":
            self.table_critic = False
            critic = NeuralNetCritic(cfg, self.game.board.generate_state())
        return critic

    def plot_result(self):
        window_size = min(cfg["display"]["plot_window_size"], int(self.episodes / 2))

        plt.figure()
        plt.plot(self.iterations, self.remaining_pegs, color='#638ed4')
        plt.plot(self.iterations[int(window_size/2):-int((window_size-1)/2)],
                 np.convolve(self.remaining_pegs, np.ones((window_size,)) / window_size, mode='valid'), color='#003182')
        plt.xlabel('Episode')
        plt.ylabel('Remaining pegs')
        plt.show()

    def play_final_game(self, SAP_history):
        self.game = self.initialize_game()
        self.visualizer.fill_nodes(self.game.board.get_filled_cells())

        for sap in SAP_history:
            action = sap[1]
            self.game.perform_action(action)
            self.visualizer.fill_nodes(
                self.game.board.get_filled_cells(), action[0], action[1]
            )

    def reset_eligibilities_and_history(self):
        self.critic.reset_eligibility()
        self.actor.reset_eligibilities()
        self.SAP_history = []

    def initialize_new_game(self):
        self.game = self.initialize_game()
        init_state = self.game.board.generate_state()  # String with state
        possible_actions = (self.game.get_all_legal_actions())  # List of actions [(from), (to)]
        self.actor.initialize_policy(init_state, possible_actions)  # Creates dictionary {string: tuple of tuple}
        init_action = self.actor.choose_action(init_state, possible_actions,
                                               epsilon_greedy=self.epsilon_greedy)  # Tuple of tuple
        if self.table_critic:
            self.critic.initialize_value_function(init_state)  # Creates dictionary {string: value}

        return init_state, init_action, possible_actions

    def get_reward_and_succ_state(self, state, action):
        """Initializes value of new states found to 0 at the start of an episode"""
        if self.table_critic:
            self.critic.initialize_value_function(state)

        """ Do action a from state s to s', and receive reward r """
        reward = self.game.perform_action(action)  # Int
        succ_state = self.game.board.generate_state()  # String

        """ Add performed action to SAP history"""
        self.SAP_history.append((state, action))

        """ Dynamically update value function if succ_state is never seen before """
        if self.table_critic:
            self.critic.initialize_value_function(succ_state)

        return reward, succ_state

    def get_succ_action(self, succ_state):
        """ Dictate a' from the current policy for s' """
        possible_succ_actions = self.game.get_all_legal_actions()

        succ_action = None
        if len(possible_succ_actions) > 0:
            """
            If succ_state has any legal actions:
            Dynamically update value function of succ_state and its possible actions
            """
            self.actor.initialize_policy(succ_state, possible_succ_actions)
            succ_action = self.actor.choose_action(succ_state, possible_succ_actions,
                                                   epsilon_greedy=self.epsilon_greedy)  # tuple of tuple
        return succ_action

    def set_eligibilities_for_current_state(self, state, action):
        """ Set eligibility of a and s to 1 """
        self.actor.set_current_eligibility(state, action)

        """ Set eligibility of current state to 1 (gets all the reward or punishment) """
        if self.table_critic:
            self.critic.set_current_eligibility(state)

    def update_eligibility_traces(self, reward, TD_error, succ_state):
        for SAP in self.SAP_history:
            state = SAP[0]
            action = SAP[1]

            self.critic.update_value_function(state, TD_error, reward, succ_state)
            if self.table_critic:
                self.critic.update_eligibility(state)

            self.actor.update_policy(state, action, TD_error)
            self.actor.update_eligibility(state, action)

    def play_game(self):
        for i in range(self.episodes):

            if i == self.episodes - 1:
                print('Switched to following policy')
                self.epsilon_greedy = False

            """ Reset all elegibilities to 0 """
            self.reset_eligibilities_and_history()

            """Initialize new game"""
            init_state, init_action, possible_actions = self.initialize_new_game()

            state = init_state  # String
            action = init_action  # Tuple of tuple

            """ Play game until termination """
            while not self.game.is_finished():

                reward, succ_state = self.get_reward_and_succ_state(state, action)
                succ_action = self.get_succ_action(succ_state)
                self.set_eligibilities_for_current_state(state, action)

                """ Compute TD error """
                TD_error = self.critic.calculate_TD_error(state, succ_state, reward)

                """ Update the eligibility traces for the path taken up to this point """
                self.update_eligibility_traces(reward, TD_error, succ_state)

                state = succ_state
                if succ_action:
                    action = succ_action

            """ Decay epsilon for each episode """
            self.actor.epsilon = self.actor.epsilon * self.actor.epsilon_decay

            pegs = self.game.get_pegs()
            print(i, ": ", pegs, ' pegs were left. Epsilon: ', self.actor.epsilon)

            """ Store result for learning plot """
            self.remaining_pegs.append(pegs)
            self.iterations.append(i)

        if self.display_last_game:
            self.play_final_game(self.SAP_history)

        self.plot_result()


def main():
    player = Player()
    player.play_game()


if __name__ == "__main__":
    main()



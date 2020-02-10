import yaml
from rules import Peg, Hex
from visualizer import Visualizer
from agent.agent import Agent

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
        self.agent = Agent(cfg)
        self.episodes = cfg['RL_system']['episodes']

    def initialize_game(self):
        game_type = cfg["game"]["type"]
        if game_type == "Peg":
            game = Peg()
        if game_type == "Hex":
            game = Hex()
        return game

    def play_game(self):
        for i in range(self.episodes):
            self.agent.TD_learning(self.game)

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



if __name__ == "__main__":
    main()

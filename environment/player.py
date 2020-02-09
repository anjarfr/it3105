import yaml
from rules import Peg, Hex
from visualizer import Visualizer

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

    def initialize_game(self):
        game_type = cfg["game"]["type"]
        if game_type == "Peg":
            game = Peg()
        if game_type == "Hex":
            game = Hex()

        return game

    def play_game(self):
        while not self.game.is_finished():
            state = self.game.board
            action = self.actor.choose_action(state, self.game.get_all_legal_actions())
            succ_state, reward = self.game.perform_action(action)
            self.critic.update_value_function(state, action, reward, succ_state)

    def translate_actions(self, actions):
        """
        Translate between actions of the form start, jump, end and action number
        """


def main():
    game_type = cfg["game"]["type"]
    if game_type == "Peg":
        game = Peg()
    if game_type == "Hex":
        game = Hex()

    display_options = cfg["display"]
    visualizer = Visualizer(game.board, game.size, game.shape, display_options)
    visualizer.fill_nodes(game.board.get_filled_cells())

    game.board.generate_state()


if __name__ == "__main__":
    main()

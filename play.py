import yaml
from rules import Peg, Hex
from visualizer import Visualizer

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


def main():
    game_type = cfg["game"]["type"]
    display_options = cfg["display"]

    if game_type == "Peg":
        game = Peg()
    if game_type == "Hex":
        game = Hex()

    visualizer = Visualizer(game.board, game.size, game.shape, display_options)
    visualizer.fill_nodes(game.board.get_filled_cells())

    game.perform_action((0, 3), (1, 2), (2, 1))
    visualizer.fill_nodes(game.board.get_filled_cells())
    game.perform_action((3, 0), (2, 1), (1, 2))
    visualizer.fill_nodes(game.board.get_filled_cells())

    for a in game.history:
        print(a.get_filled_cells())

    print(game.board.get_filled_cells())


if __name__ == "__main__":
    main()

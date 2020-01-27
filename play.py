import yaml
from game import Peg, Hex
from visualizer import Visualizer

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


def main():
    game_type = cfg['game']['type']
    display_options = cfg['display']

    if game_type == 'Peg': game = Peg()
    if game_type == 'Hex': game = Hex()

    visualizer = Visualizer(game.board, game.size, game.shape, display_options)
    visualizer.display_board()
    visualizer.fill_nodes([(2, 1), (0, 1), (0, 0)])


if __name__ == '__main__':
    main()

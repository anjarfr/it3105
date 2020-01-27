import yaml
from game import Peg, Hex
from display_game import display_game_board

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def main():
    game_type = cfg['game']['type']
    if game_type == 'Peg': game = Peg()
    if game_type == 'Hex': game = Hex()
    display_game_board(game.board, game.size, game.shape)


if __name__ == '__main__':
    main()
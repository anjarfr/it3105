import yaml
from board import create_board, set_cell, get_cell_coord, get_neighbors_triangle
from display_game import display_game_board

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Game:

    def __init__(self):
        self.size = cfg['board']['size']
        self.shape = cfg['board']['shape']
        self.board = create_board(self.shape, self.size)
    
    def terminal_print(self):
        for row in self.board:
            for cell in row:
                print(cell.state) if cell != None else print(cell)


class Peg(Game):
    
    def __init__(self):
        super(Peg, self).__init__()
        self.open_positions = cfg['game']['open_positions']
        self.board = self.place_pieces(self.board, self.open_positions)
        
    def place_pieces(self, board: object, open_positions):
        for r in range(board.size):
            for c in range(board.size):
                coordinate = [r, c]
                if coordinate not in open_positions:
                   set_cell(board, r, c, (0,1))
        return board


class Hex(Game):
    pass

def main():
    game_type = cfg['game']['type']
    if game_type == 'Peg': game = Peg()
    if game_type == 'Hex': game = Hex()
    display_game_board(game.board, game.size, game.shape)


if __name__ == '__main__':
    main()

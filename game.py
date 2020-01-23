import yaml
from board import Board

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

class Game:
    pass

class Peg(Game):
     
    def __init__(self, open_positions: list, k: int=1):
        self.k = k
        self.board = self.init_board(open_positions)

    def init_board(self, open_positions: list):
        board = Board(cfg['board']['shape'], cfg['board']['size'])
        for r in range(board.size):
            for c in range(board.size):
                coordinate = (r, c)
                if coordinate in open_positions:
                    continue

                board.set_cell(r, c, (0,1))
        return board
        
    def place_pieces(self, board: object):
        pass


p = Peg(cfg['game']['open_positions'], cfg['game']['open_cells'])
print(p.board.board)
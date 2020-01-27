import yaml
from board import create_board, set_cell, get_neighbors_triangle

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
    # All rules and legal actions related to the Peg game
    
    def __init__(self):
        super(Peg, self).__init__()
        self.open_positions = cfg['game']['open_positions']
        self.board = self.place_pieces(self.board, self.open_positions)
        
    def place_pieces(self, board: object, open_positions):
        for r in range(self.size):
            for c in range(self.size):
                coordinate = [r, c]
                if coordinate not in open_positions:
                   set_cell(board, r, c, (0,1))
        return board

    def get_legal_actions(self, coord: tuple, peg: object):
        # returns all legal moves for the specified peg
        filled = []
        moves = []
        neighbors = get_neighbors_triangle
            

        pass

    def act(self, start, end):
        # perform the action chosen by Actor/Critic
        pass

    


class Hex(Game):
    pass

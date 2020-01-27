import yaml
from board import Triangle, Diamond
from display_game import display_game_board

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Game:

    def __init__(self):
        self.size = cfg['board']['size']
        self.shape = cfg['board']['shape']

        if self.shape == 'triangle':
            self.board = Triangle(self.size)
        if self.shape == 'diamond':
            self.board = Diamond(self.size)
    
    def terminal_print(self):
        for row in self.board.cells:
            for cell in row:
                print(cell.state, cell.coordinates) if cell != None else print(cell)


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
                   self.board.set_cell(r, c, (0,1))
        return board

    def get_legal_actions(self, r, c):
        # returns all legal moves for the peg in the specified coordinate (r, c)
        
        legal_moves = {}
        neighbors = self.board.get_neighbors(self.size, r, c)

        for node in neighbors:
            row = node[0]
            col = node[1]
            cell = self.board.cells[row][col]
            # for all neighboring cells that are filled
            if cell != None and cell.is_filled():
                # find the possible cell to jump to
                row_diff, col_diff = (node[0] - r, node[1] - c)
                target_row, target_col = r + 2*row_diff, c + 2*col_diff
                if self.board.is_legal_cell(target_row, target_col):
                    target_cell = self.board.cells[target_row][target_col]
                    # if that cell is empty
                    if not target_cell.is_filled():
                        # the peg can jump here!
                        legal_moves[(target_row, target_col)] = target_cell
        return legal_moves
            
    def perform_action(self, start, end):
        # perform the action chosen by Actor/Critic
        self.board.set_cell(start[0], start[1], (0,0))
        self.board.set_cell(end[0], end[1], (0,1))
    


class Hex(Game):
    pass

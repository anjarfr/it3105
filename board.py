import numpy as np
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def create_triangle(size):
    board = np.empty((size, size), dtype='object')
    iterator = 1
    while iterator != size + 1:
        for row in board:
            for i in range(iterator):
                row[i] = Cell((0,0))
            iterator += 1
    return board

def create_diamond(size):
    board = np.empty((size, size), dtype='object')
    for row in board:
        for i in range(row.size):
            row[i] = Cell((0,0))
    return board

def create_board(shape, size):
    if shape == 'triangle':
        return create_triangle(size)
    if shape == 'diamond':
        return create_diamond(size)

def set_cell(board, r, c, state):
    try:
        board[r][c].set_state(state)
    except:
        pass


class Cell:
    """
    Represents a cell in the board. Has a state that can have
    3 values: (0,0) - emtpy, (0,1) - player 1, (1,0) - player 2
    """
    
    def __init__(self, state):  
        self.state = state
        self.visited = False
    
    def set_visited(self, visited):
        self.visited = visited

    def set_state(self, state):
        self.state = state


#b = Board(cfg['board']['shape'], cfg['board']['size'])
#print(b.board)
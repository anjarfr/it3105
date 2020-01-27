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


def get_cell_coord(board):
    return list(zip(*np.where(board != None)))


def get_neighbors_triangle(size, r, c):
    tmp = [ (r-1, c-1), (r-1, c),
            (r, c-1),   (r, c+1),
            (r+1, c),   (r+1, c+1) ]
    neighbors = []          
    for cell in tmp:
        row = cell[0]
        col = cell[1]
        if row < 0 or row > size-1 or col < 0 or col > row:
            continue
        neighbors.append(cell)    
    return neighbors


def get_neighbors_diamond(size, r, c):
    tmp = [ (r-1, c),   (r-1, c+1), 
            (r, c-1),   (r, c+1),
            (r+1, c-1), (r+1, c) ]
    neighbors = []          
    for cell in tmp:
        row = cell[0]
        col = cell[1]
        if row < 0 or row > size-1 or col < 0 or col > size-1:
            continue
        neighbors.append(cell)    
    return neighbors

def get_neighbors(shape, size, r, c):
    if shape == 'triangle':
        return get_neighbors_triangle(size, r, c)
    if shape == 'diamond':
        return get_neighbors_diamond(size, r, c)
    return None


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



import numpy as np

class Board:
    
    def __init__(self, size):
        self.size = size
        self.cells = self.create_board(self.size)

    def create_board(self, size):
        pass

    def set_cell(self, board, r, c, state):
        try:
            self.cells[r][c].set_state(state)
        except:
            pass

    def get_cell_coord(self):
        return list(zip(*np.where(self.board != None)))


class Triangle(Board):

    def __init__(self, size):
        super(Triangle, self).__init__(size)

    def create_board(self, size):
        cells = np.empty((size, size), dtype='object')
        iterator = 1
        while iterator != size + 1:
            for row in cells:
                for i in range(iterator):
                    row[i] = Cell((0,0))
                iterator += 1
        return cells

    def get_neighbors(self, size, r, c):
        tmp = [ (r-1, c-1), (r-1, c),
                (r, c-1),   (r, c+1),
                (r+1, c),   (r+1, c+1) ]
        neighbors = []          
        for cell in tmp:
            row = cell[0]
            col = cell[1]
            if self.is_illegal_cell(row, col):
                continue
            neighbors.append(cell)    
        return neighbors

    def is_illegal_cell(self, row, col):
        return row < 0 or row > self.size-1 or col < 0 or col > row

    
class Diamond(Board):

    def __init__(self, size):
        super(Diamond, self).__init__(size)

    def create_board(self, size):
        cells = np.empty((size, size), dtype='object')
        for row in cells:
            for i in range(row.size):
                row[i] = Cell((0,0))
        return cells

    def get_neighbors(self, size, r, c):
        tmp = [ (r-1, c),   (r-1, c+1), 
                (r, c-1),   (r, c+1),
                (r+1, c-1), (r+1, c) ]
        neighbors = []          
        for cell in tmp:
            row = cell[0]
            col = cell[1]
            if self.is_illegal_cell(row, col):
                continue
            neighbors.append(cell)
        return neighbors

    def is_illegal_cell(self, row, col):
        return row < 0 or row > self.size-1 or col < 0 or col > self.size-1


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

    def is_filled(self):
        return self.state != (0, 0)


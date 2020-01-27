import numpy as np

class Board:
    
    def __init__(self, size):
        self.size = size
        self.cells = self.create_board(self.size)

    def create_board(self, size):
        pass

    def set_cell(self, r, c, state):
        try:
            self.cells[r][c].set_state(state)
        except:
            pass

    def get_cell_coord(self):
        return list(zip(*np.where(self.cells != None)))

    def get_filled_cells(self):
        filled = []
        for row in self.cells:
            for cell in row:
                if cell.is_filled(): filled.append(cell.coordinates)
        return filled


class Triangle(Board):

    def __init__(self, size):
        super(Triangle, self).__init__(size)

    def create_board(self, size):
        cells = np.empty((size, size), dtype='object')
        iterator = 1
        while iterator != size + 1:
            for row in range(size):
                for col in range(iterator):
                    cells[row][col] = Cell((0,0), (row, col))
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
            if self.is_legal_cell(row, col):
                neighbors.append(cell)    
        return neighbors

    def is_legal_cell(self, row, col):
        return not (row < 0 or row > self.size-1 or col < 0 or col > row)

    
class Diamond(Board):

    def __init__(self, size):
        super(Diamond, self).__init__(size)

    def create_board(self, size):
        cells = np.empty((size, size), dtype='object')
        for row in range(size):
            for col in range(size):
                cells[row][col] = Cell((0,0), (row, col))
        return cells

    def get_neighbors(self, size, r, c):
        tmp = [ (r-1, c),   (r-1, c+1), 
                (r, c-1),   (r, c+1),
                (r+1, c-1), (r+1, c) ]
        neighbors = []          
        for cell in tmp:
            row = cell[0]
            col = cell[1]
            if self.is_legal_cell(row, col):
                neighbors.append(cell)
        return neighbors

    def is_legal_cell(self, row, col):
        return not (row < 0 or row > self.size-1 or col < 0 or col > self.size-1)


class Cell:
    """
    Represents a cell in the board. Has a state that can have
    3 values: (0,0) - emtpy, (0,1) - player 1, (1,0) - player 2
    """
    
    def __init__(self, state, coordinates):  
        self.state = state
        self.visited = False
        self.coordinates = coordinates
    
    def set_visited(self, visited):
        self.visited = visited

    def set_state(self, state):
        self.state = state

    def is_filled(self):
        return self.state != (0, 0)


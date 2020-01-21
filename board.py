import numpy as np

class Board:

    def __init__(self, size=3):
        self.size = size
        self.board = self.create_board()

    def create_board(self):
        return None

class Triangle(Board):
    
    def __init__(self, size):
        super(Triangle, self).__init__(size)

    def create_board(self):
        board = np.empty((self.size, self.size), dtype='object')
        iterator = 1
        while iterator != self.size + 1:
            for row in board:
                for i in range(iterator):
                    row[i] = Cell(0)
                iterator += 1
        return board


class Diamond(Board):

    def __init__(self, size):
        super(Diamond, self).__init__(size)

    def create_board(self):
        board = np.empty((self.size, self.size), dtype='object')
        for row in board:
            for i in range(row.size):
                row[i] = Cell(0)
        return board


class Cell:
    """
    
    """
    
    def __init__(self, state):  
        self.state = state
        self.visited = False
    
    def set_visited(self, visited):
        self.visited = visited

    def set_state(self, state):
        self.state = state


t = Triangle(5)
#print(t.board)
d = Diamond(5)
print(d.board)
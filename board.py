import numpy as np

class Board:

    def __init__(self, size=3):
        self.size = size

    def create_board(self):
        print('5')



class Triangle(Board):
    
    def __init__(self, size):
        super(Triangle, self).__init__(size)

    def create_board(self):
        print('4')


class Diamond(Board):
    pass


class Cell:
    """
    
    """
    
    def __init__(self, state):  
        self.state = state
        self.visited = False
    
    def set_visited(self, visited):
        self.visited = visited

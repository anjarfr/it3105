import yaml
from copy import deepcopy
from board import Triangle, Diamond

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Game:
    def __init__(self):
        self.size = cfg["board"]["size"]
        self.shape = cfg["board"]["shape"]
        self.history = []

        if self.shape == "triangle":
            self.board = Triangle(self.size)
        if self.shape == "diamond":
            self.board = Diamond(self.size)

    def terminal_print(self):
        # Simple printout of all cell states in board
        for row in self.board.cells:
            for cell in row:
                print(cell.state, cell.coordinates) if cell != None else print(cell)


class Peg(Game):
    """ All rules and legal actions related to the Peg game """

    def __init__(self):
        super(Peg, self).__init__()
        self.open_positions = cfg["game"]["open_positions"]
        self.board = self.place_pieces(self.board, self.open_positions)

    def place_pieces(self, board: object, open_positions):
        """ Initialize all pegs """
        for r in range(self.size):
            for c in range(self.size):
                coordinate = [r, c]
                if coordinate not in open_positions and self.board.is_legal_cell(r, c):
                    self.board.set_cell(r, c, (0, 1))
        return board

    def get_legal_actions(self, r: int, c: int):
        """
        Returns all legal moves for the peg in the specified coordinate (r, c)
        as a list of coordinates the peg can jump to
        """

        legal_actions = []

        neighbors = self.board.get_neighbors(r, c)

        for node in neighbors:
            row = node[0]
            col = node[1]
            cell = self.board.cells[row][col]

            # If the current neighboring cell is filled
            if cell != None and cell.is_filled():

                # Find the target cell to possibly jump to
                # There is only one
                row_diff, col_diff = (row - r, col - c)
                target_row, target_col = r + 2 * row_diff, c + 2 * col_diff

                if self.board.is_legal_cell(target_row, target_col):
                    target_cell = self.board.cells[target_row][target_col]

                    # If that cell is emptyhttps://stackoverflow.com/questions/8322534/typeerror-builtin-function-or-method-object-is-not-subscriptable
                    if not target_cell.is_filled():

                        # The peg can jump over node to get to target cell!
                        legal_actions.append((target_row, target_col))

        return legal_actions

    def search_legal_actions(self):
        # TODO
        """
        Return all possible legal actions from the board
        """
        legal_actions = {}
        for row in range(self.size):
            for col in range(self.size):
                actions = self.get_legal_actions(row, col)
                if len(actions) > 0:
                    legal_actions[(row, col)] = actions
        return legal_actions

    def perform_action(self, start: tuple, end: tuple):
        """
        Perform the action chosen by Actor/Critic.
        Appends the previous board state to history.
        Returns the new state and the given reward
        from that action, given state
        """

        self.history.append(self.board)

        self.board = deepcopy(self.board)

        # Calculate which cell the peg jumps over
        row_diff = start[0] - end[0]
        col_diff = start[1] - end[1]
        jump = (int(start[0] - row_diff / 2), int(start[1] - col_diff / 2))

        # Remove the peg in start position and the peg it jumps over
        self.board.set_cell(start[0], start[1], (0, 0))
        self.board.set_cell(jump[0], jump[1], (0, 0))
        self.board.set_cell(end[0], end[1], (0, 1))

        reward = 0
        if self.is_finished():
            reward = 100

        return self.board, reward

    def get_pegs(self):
        return len(self.board.get_filled_cells())

    def is_finished(self):
        return self.get_pegs() == 1


class Hex(Game):
    pass

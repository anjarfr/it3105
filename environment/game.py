import yaml
from environment.board import Triangle, Diamond

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Game:
    def __init__(self):
        self.size = cfg["board"]["size"]
        self.shape = cfg["board"]["shape"]

        if self.shape == "triangle":
            self.board = Triangle(self.size)
        if self.shape == "diamond":
            self.board = Diamond(self.size)

    def terminal_print(self):
        # Simple printout of all cell states in board
        for row in self.board.cells:
            rowstring = ""
            for cell in row:
                if cell != None:
                    rowstring += str(cell.state[1]) + " "
            print(rowstring)
        print("--------")


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

                    # If that cell is empty
                    if not target_cell.is_filled():

                        # The peg can jump over node to get to target cell!
                        legal_actions.append((target_row, target_col))

        return legal_actions

    def get_all_legal_actions(self):
        """
        Return all possible legal actions from the board
        """
        legal_actions = []

        # For all cells
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board.cells[row][col]

                # If this is a legal cell and there is a peg here
                if self.board.is_legal_cell(row, col) and cell.is_filled():

                    # Find all positions the peg can jump to
                    actions = self.get_legal_actions(row, col)

                    if len(actions) > 0:
                        for jump_to in actions:
                            jump_from = (row, col)
                            legal_actions.append((jump_from, jump_to))

        return legal_actions

    def perform_action(self, action: tuple):
        """
        Perform the action chosen by Actor/Critic.
        Appends the previous board state to history.
        Returns the new state and the given reward
        from that action, given state
        """

        start = action[0]
        end = action[1]

        # Calculate which cell the peg jumps over
        row_diff = start[0] - end[0]
        col_diff = start[1] - end[1]
        jump = (int(start[0] - row_diff / 2), int(start[1] - col_diff / 2))

        # Remove the peg in start position and the peg it jumps over
        self.board.set_cell(start[0], start[1], (0, 0))
        self.board.set_cell(jump[0], jump[1], (0, 0))
        self.board.set_cell(end[0], end[1], (0, 1))

        reward = 0

        if self.is_in_goal_state():
            reward = 1000
        elif self.no_more_actions():
            reward = -1*self.get_pegs()

        return reward

    def get_pegs(self):
        return len(self.board.get_filled_cells())

    def is_in_goal_state(self):
        return self.get_pegs() == 1

    def no_more_actions(self):
        return len(self.get_all_legal_actions()) == 0

    def is_finished(self):
        return self.is_in_goal_state() or self.no_more_actions()


class Hex(Game):
    pass

import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self, board, size, shape, display_options):
        self.board = board
        self.size = size
        self.shape = shape

        self.node_size = display_options['node_size']
        self.initial_color = display_options['initial_color']
        self.filled_color = display_options['filled_color']

        self.nodes = self.get_nodes()
        self.positions = self.get_positions()
        self.edges = self.get_edges()
        self.node_colors = self.initialize_colors()
        self.graph = self.initialize_graph()

    def get_nodes(self):
        return self.board.get_cell_coord()

    def get_positions(self):
        positions = {}
        counter = 0

        if self.shape == 'triangle':
            for i in range(self.size + 1):
                for j in range(-i, i, 2):
                    positions[self.nodes[counter]] = [self.size + j, self.size - i]
                    counter += 1

        if self.shape == 'diamond':
            for i in range(self.size, 0, -1):
                for j in range(self.size):
                    positions[self.nodes[counter]] = [i + j, i - j]
                    counter += 1

        return positions

    def get_edges(self):
        edges = []

        for node in self.nodes:
            neighbors = self.board.get_neighbors(self.size, node[0], node[1])
            edges += [(node, x) for x in neighbors]

        return edges

    def initialize_colors(self):
        return [self.initial_color for i in range(len(self.nodes))]

    def initialize_graph(self):

        G = nx.Graph()
        G.add_nodes_from(self.nodes)
        G.add_edges_from(self.edges)

        return G

    def fill_nodes(self, fill_nodes):
        filled_indexes = [self.nodes.index(node) for node in fill_nodes]

        for index in filled_indexes:
            self.node_colors[index] = self.filled_color

        self.display_board()

    def display_board(self):
        plt.figure(figsize=(10, 10))
        nx.draw_networkx(self.graph, pos=self.positions, node_color=self.node_colors, node_size=self.node_size,
                         edgecolors='black')
        plt.axis('off')
        plt.show()


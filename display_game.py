import networkx as nx
import matplotlib.pyplot as plt
from board import get_cell_coord


def display_game_board(board, size, shape):
    options = {
        'node_size': 1000,
        'node_color': range(15),
        'cmap':  plt.cm.Blues
        }

    nodes = get_cell_coord(board)
    #nodes = [*range(0, int((size*size + size) / 2), 1)]
    positions = {}

    for i in range(size + 1):
        for j in range(-i, i, 2):
            positions[nodes.pop(0)] = [size+j, size-i]

    plt.figure(figsize=(10, 10))
    G = nx.Graph()

    G.add_nodes_from(nodes)

    # Color nodes (filled / empty)
    color_map = []
    for node in G:
        if node:
            color_map.append('lightBlue')
        else:
            color_map.append('lightGreen')

    #G.add_edges_from([(0,1),(1,2),(2,3),(3,0), (3,1), (4,1), (5,2), (6,2), (7,2), (8,2)])
    nx.draw_networkx(G, pos=positions, **options)

    plt.axis('off')
    plt.show()
    # plt.savefig("path.png")



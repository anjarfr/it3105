import networkx as nx
import matplotlib.pyplot as plt
from board import get_cell_coord, get_neighbors_triangle, get_neighbors_diamond


def display_game_board(board, size, shape):
    options = {
        'node_size': 100,
        'node_color': 'black',
        }

    G = nx.Graph()

    nodes = get_cell_coord(board)
    G.add_nodes_from(nodes)

    positions = {}
    counter = 0

    if shape == 'triangle':
        for i in range(size + 1):
            for j in range(-i, i, 2):
                positions[nodes[counter]] = [size+j, size-i]
                counter += 1


    if shape == 'diamond':
        for i in range(size, 0, -1):
            for j in range(size):
                positions[nodes[counter]] = [i+j, i-j]
                counter += 1


    edges = []
    for node in nodes:
        if shape == 'triangle':
            neighbors = get_neighbors_triangle(board, size, shape, node[0], node[1])
        else:
            neighbors = get_neighbors_diamond(board, size, shape, node[0], node[1])
        edges += [(node, x) for x in neighbors]

    G.add_edges_from(edges)

    plt.figure(figsize=(10, 10))

    # Color nodes (filled / empty)
    color_map = []
    for node in G:
        if node:
            color_map.append('lightBlue')
        else:
            color_map.append('lightGreen')

    nx.draw_networkx(G, pos=positions, **options)

    plt.axis('off')
    plt.show()
    # plt.savefig("path.png")





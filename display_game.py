import networkx as nx
import matplotlib.pyplot as plt


def display_game_board(board, size, shape):
    options = {
        'node_size': 100,
        'node_color': 'black',
        }

    G = nx.Graph()

    nodes = board.get_cell_coord()
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
        neighbors = board.get_neighbors(shape, size, node[0], node[1])
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





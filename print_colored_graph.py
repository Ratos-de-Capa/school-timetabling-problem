import matplotlib.pyplot as plt
import networkx as nx

# Criar um grafo simples
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])

# Atribuir cores aos vértices
node_colors = [1, 2, 3, 4]

# Desenhar o grafo
pos = nx.spring_layout(G)  # Posicionamento dos vértices
nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, node_size=700)

# Exibir o gráfico
plt.show()


def print_colored_graph_from_dict(dict):
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])

    # Atribuir cores aos vértices
    node_colors = [1, 2, 3, 4]

    # Desenhar o grafo
    pos = nx.spring_layout(G)  # Posicionamento dos vértices
    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, node_size=700)

    # Exibir o gráfico
    plt.show()
    
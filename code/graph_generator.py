########################################################
### Fichier pour générer des graphes et les afficher ###
########################################################

import graph_type
import networkx as nx
import matplotlib.pyplot as plt

G = graph_type.gen_erdos_reyni(200, 0.05)
nx.write_gexf(G, "game_graph.gexf")

positions = nx.spring_layout(G)
fig, ax = plt.subplots()

nx.draw(G, pos=positions, ax=ax, node_size=150, with_labels=True)

plt.show()

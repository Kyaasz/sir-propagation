###############################################
### Fichier pour visualiser un graphe donné ###
###############################################

import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_gexf("game_graph.gexf", node_type=int)
positions = nx.spring_layout(G)
_, ax = plt.subplots()
nx.draw(G, pos=positions, ax=ax, node_size=30, with_labels=False)
plt.show()

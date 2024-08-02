########################################################
### Fichier pour générer des graphes et les afficher ###
########################################################

import graph_type
import random
import networkx as nx
import matplotlib.pyplot as plt

nb_noeuds = random.randint(900,1100)
G = graph_type.small_word_network(nb_noeuds, 4, 1)
nx.write_gexf(G, "delta_game_sw.gexf")

positions = nx.spring_layout(G)
fig, ax = plt.subplots()

nx.draw(G, pos=positions, ax=ax, node_size=150, with_labels=True)

plt.show()

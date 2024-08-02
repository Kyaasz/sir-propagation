#########################################################################
### Fichier pour la génération de données pour le jeu virus-antivirus ###
#########################################################################

import game
import networkx as nx
import matplotlib.pyplot as plt
import Delta_time_fun
import csv

G = nx.read_gexf("delta_game.gexf", node_type=int)
N = G.number_of_nodes()
K_tab = [i for i in range(0, 200)]
alpha = 1
beta = 5
sim_nb = 30
############ unicast 


EP_tab = []
TAB_tab = []
cost_tab = []
delta = []

for k in K_tab: 
    print("Simu")
    ep = 0
    tab = []
    for i in range(sim_nb):
        ep_temp, inf_tab = game.unicast_competing_propagation(G, [0], 0, 1, 1, k)
        ep = ep_temp + ep
        tab.append(inf_tab)
    ep = ep/sim_nb
    EP_tab.append(ep)
    TAB_tab.append(tab)
    cost_tab.append(alpha * ep + beta* k*1000/N)

for k in K_tab: 
    delta.append(Delta_time_fun.delta_fun(k))


## sauvegarde des résultats

rows = zip(K_tab, EP_tab, TAB_tab, cost_tab, delta)
headers = ["K", "epidemic peak", "nombre infectes", "cost fun", "delta fun"]
with open('competing_virus_antivirus/game_theory/res_simu/cost_little_graph_unicast_virus2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)



############ broadcast 

EP_tab = []
TAB_tab = []
cost_tab = []
delta = []

for k in K_tab: 
    print("Simu")
    ep = 0
    tab = []
    for i in range(sim_nb):
        ep_temp, inf_tab = game.broadcast_competing_propagation(G, [0], 0, 1, 1, k)
        ep = ep_temp + ep
        tab.append(inf_tab)
    ep = ep/sim_nb
    EP_tab.append(ep)
    TAB_tab.append(tab)
    cost_tab.append(alpha * ep + beta* k*1000/N)

for k in K_tab: 
    delta.append(Delta_time_fun.delta_fun(k))


## sauvegarde des résultats

rows = zip(K_tab, EP_tab, TAB_tab, cost_tab, delta)
headers = ["K", "epidemic peak", "nombre infectes", "cost fun", "delta fun"]
with open('competing_virus_antivirus/game_theory/res_simu/cost_little_graph_broadcast_virus2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)





## affichage des résultats

plt.figure(1)
plt.plot(K_tab, EP_tab)
plt.plot(K_tab, cost_tab)
plt.xlabel("Valeur du coût K (en milliers d'euros)")
plt.ylabel("Fonction de coût")
plt.title("Evolution de la fonction de coût en fonction de l'investissement")
plt.legend({"epidemic peak", "cost"})
plt.figure(2)
plt.plot(K_tab, delta)
plt.xlabel("Valeur du coût K (en milliers d'euros)")
plt.ylabel("Temps Delta de la mise en place de l'antivirus")
plt.title("Evolution du temps Delta en fonction de l'investissement")
plt.show()       

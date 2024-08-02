#################################################################################
### Fichier pour la génération de données pour le premier jeu virus-antivirus ###
#################################################################################

import game
import networkx as nx
import matplotlib.pyplot as plt
import Delta_time_fun
import csv
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import time

G = nx.read_gexf("delta_game.gexf", node_type=int)
N = G.number_of_nodes()
K_tab = [i for i in range(200,1600,10)]
"""K_tab = [x/2 for x in K_tab]"""
delta = []
alpha = 1
beta = 180
sim_nb = 1

def fun(k):
    print("debut simu")
    ep = 0
    for i in range(sim_nb):
        d = time.time()
        ep += game.unicast_competing_propagation(G, [0], 0, 1, 1, k)
        print(f"temps : {time.time() - d}")
    ep = ep/sim_nb
    print("fin simu")
    return(ep, alpha * ep + beta* k*1000/N)
    


res = Parallel(n_jobs=cpu_count())(delayed(fun)(k) for k in K_tab)

EP_tab = [r[0] for r in res]
cost_tab = [r[1] for r in res]
for k in K_tab: 
    delta.append(Delta_time_fun.delta_fun(k))


## sauvegarde des résultats

rows = zip(K_tab, EP_tab, cost_tab, delta)
headers = ["K", "epidemic peak", "cost fun", "delta fun"]
with open('competing_virus_antivirus/game_theory/res_simu/big_graph_unicast_virus_parallel9_beta.csv', 'w', newline='') as f:
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

########################################################################################
### Fichier de génération parallélisée de données pour le ML avec différents graphes ###
########################################################################################

import attack_app2_gen
import math
import csv 
import numpy as np
import networkx as nx
import random
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import graph_type
import time


nb_simu = 3000 ### nombre de simulation par type de propagation


# lancement d'une simulation        
def simu(p,i):
    nb_noeuds = random.randint(80, 150)
    pts = graph_type.gen_in_disk(nb_noeuds)
    G = graph_type.delaunay_graph(pts)
    nb_aretes = G.number_of_edges()
    liste_degre = [deg for _,deg in G.degree()]
    deg_moyen = np.mean(liste_degre)
    deg_min = np.min(liste_degre)
    deg_max = np.max(liste_degre)
    dist_moyenne = nx.average_shortest_path_length(G)
    carac_graphe = [nb_noeuds, nb_aretes, deg_moyen, deg_min, deg_max, dist_moyenne]
    print(f"Début simulation {p+1}, {i}")

    temp = []
    temp.extend(carac_graphe)
    temp.append((p+1))

    propor = random.uniform(0,1)
    match p:
        case 1:
            temp.append(propor)
        case _:
            temp.append(-1)

    ### simulation
    alpha = random.uniform(0.001, 0.1)
    prob = random.uniform(0.01, 0.3)
    begin = random.choice(list(G.nodes))
    deg_source = liste_degre[begin]
    nb_honey = random.randint(0,math.floor(0.08*nb_aretes))
    nb_smart = random.randint(0, math.floor(nb_honey/2))
    temp.extend([nb_honey, nb_smart, prob, alpha, deg_source])

    match p:
        case 0:
            inf5, res5, pic, tte = attack_app2_gen.propagation_unicast([begin], G, [], alpha, prob, nb_honey, nb_smart)
        case 1:
            inf5, res5, pic, tte = attack_app2_gen.propagation_probability([begin], G, [], alpha, prob, nb_honey, propor, nb_smart)
        case 2:
            inf5, res5, pic, tte = attack_app2_gen.propagation_broadcast([begin], G, [], alpha, prob, nb_honey, nb_smart)
        case 3: 
            inf5, res5, pic, tte = attack_app2_gen.propagation_deterministic_smart([begin], G, [], alpha, prob, nb_honey, nb_smart)
        case 4:
            inf5, res5, pic, tte = attack_app2_gen.propagation_probabilistic_smart([begin], G, [], alpha, prob, nb_honey, nb_smart)
        case 5: 
            inf5, res5, pic, tte = attack_app2_gen.propagation_broadcast_smart([begin], G, [], alpha, prob, nb_honey, nb_smart)
        case _:
            pass

    temp.extend([inf5, res5, pic, tte])
    print(f"Fin simulation {p+1}, {i}")
    return temp

### run parallel
debut = time.time()
resultats = Parallel(n_jobs=cpu_count())(delayed(simu)(p,i) for p in range(6) for i in range(nb_simu))
temps_ex = time.time() - debut
print("=========================================== Fin des simulations ===================================================")

## écriture du csv 
with open('resultats14.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    headers = ["nombre de noeuds", "nombre d'aretes", "degre moyen", "degre minimal", "degre maximal", "distance moyenne", "dynamique de propagation", "proportion propagation", "nombre de honeypots", "nombre de smart honeypots", "probabilite I -> S", "probabilite S -> R", "degre du noeud source", "nombre inf 5", "nombre res 5", "epidemic peak", "time to extinction"]
    writer.writerow(headers)
    writer.writerows(resultats)
print(f"Temps d'execution : {temps_ex}")
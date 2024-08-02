################################################################################################################################
### Fichier qui génère les données de simulation pour le jeu attaquant-défenseur basé sur le premier modèle (avec honeypots) ###
################################################################################################################################

import attack_app2_gen_game
import networkx as nx
import time
import csv
from joblib import Parallel, delayed
from multiprocessing import cpu_count

# graphe
G = nx.read_gexf("game_graph.gexf", node_type=int)

# variables des simulations

is_tab = [i/100 for i in range(10, 61, 5)]
sr_tab = [i/1000 for i in range(10, 61, 5)]
hp_tab = [i for i in range(1,6,1)]
shp_tab = [i for i in range(5)]

print("nb simu :", len(is_tab)*len(sr_tab)*len(hp_tab)*len(shp_tab))
nb_simu = 3

## fonction de simulation, tous les paramètres étant donnés
def simu(i_s, s_r, hp, shp):
    print("simu")
    temp = []
    temp.extend([i_s, s_r, hp, shp])
    epm = 0
    cumulm = 0
    nb_srm = 0
    nb_ism = 0
    temp_t = time.time()
    for _ in range(nb_simu):
        ep, cumul, nb_sr, nb_is = attack_app2_gen_game.propagation_broadcast([0], G, [], s_r, i_s, hp+shp, shp)
        epm += ep
        cumulm += cumul
        nb_srm += nb_sr 
        nb_ism += nb_is
    print("temps d'une simu:", time.time()-temp_t)
    epm = epm/nb_simu
    nb_srm = nb_srm/nb_simu
    nb_ism = nb_ism/nb_simu
    cumulm = cumulm/nb_simu
    temp.extend([epm, cumulm, nb_srm, nb_ism])
    return temp

td = time.time()
resultats =  Parallel(n_jobs=cpu_count())(delayed(simu)(i_s,s_r, hp, shp) for i_s in is_tab for s_r in sr_tab for hp in hp_tab for shp in shp_tab)
tf = time.time()

print(f"temps total execution script : {tf-td}")

## écriture des résultats
with open('resultats_simu_cout_chgts.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    headers = ["proba is", "proba sr", "nombre hpb", "nombre shp", "pic", "cumul inf", "nb changements sr", "nb changements is"]
    writer.writerow(headers)
    writer.writerows(resultats)


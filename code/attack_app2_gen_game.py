################################################################################################
### Fichier qui génère la simulation sans l'aspect animation - pour la génération de données ###
################################################################################################


import numpy as np
import random
import numpy
import networkx as nx


################################################################################################
# Simule la propagation du virus avec la troisième dynamique de propagation : chaque noeud     #
# infecté transmet le virus à tous ses voisins                                                 #
# Inputs :                                                                                     #
# - begin : liste des noeuds infectés au début de la simulation                                #
# - G : graphe                                                                                 #
# - resist : noeuds résistants au début de la simulation                                       #
# - alpha : proba de faire S -> R                                                              #
# - prob : proba de faire I -> S                                                               #
# - nbr : nombre de honeypots                                                                  #
# - nbr_smart : nombre de ces honeypots qui sont intelligents                                  #
################################################################################################

def propagation_broadcast(begin, G, resist, alpha, prob, nbr, nbr_smart):

    p_inf = 0.5 ## probabilité d'infection d'un voisin
    sr_bool = False  ## booléen qui indique si la distribution d'antivirus a commencé
    inf_nb = []   ## tableau qui track le nombre d'infectés à chaque instant
    state = [0] * G.number_of_nodes() ### Tous les noeuds sont initialement susceptibles
    liste_neighbors = [list(G.neighbors(n)) for n in G.nodes] ### liste des listes de voisins
    seuil_sr = int(G.number_of_nodes()*0.05)  ## seuil à partir duquel l'antivirus commence à être déployé
    nb_is = 0  ## nombre de changements d'états i -> s
    nb_sr = 0  ## nombre de changements d'états s -> r

    # initialement, aucun sommet n'a été visité/traité
    nx.set_node_attributes(G, False, 'visited')
                
    ### Mise à jour des états avec les infectés de base 
    state = begin_node(begin, state, G)
    n_i = len(begin)
    inf_nb.append(n_i)
    sr_bool = (seuil_sr <= n_i)

    ### Arêtes résistantes   
    liste_resist = resist_list(resist, state, G)

    # on ajoute les honeypot à traiter
    honeypot1 = honey_pot(G, [], [], resist, [], liste_resist, nbr, 0)
    
    while (1 in state and (not sr_bool)):
        liste = [0] * len(state)
        liste_edge = []
        liste_node = []
        nodes_out = []
        nodes_in = []

        for n in G.nodes:  
            if (state[n]==1): 
                neighbors = liste_neighbors[G.nodes[n]['index']][:]
                suscep_neighbors = [v for v in neighbors if state[v] == 0]
                for t in suscep_neighbors:
                    if (not G.nodes[t]['visited'] and random.random()<p_inf):
                            G.nodes[t]['visited'] = True
                            edge_index = G[n][t]['index']
                            liste[t] = 1
                            if edge_index in honeypot1:
                                liste_edge.append(G[n][t]['index'])
                                liste_node.extend([n,t])
                                nodes_out.append(n)
                                nodes_in.append(t)         
        
        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                            
            G.nodes[i]['visited'] = False

        n_i = len([s for s in state if s == 1]) + len([l for l in liste if l==1])
        inf_nb.append(n_i)
        sr_bool = n_i >= seuil_sr

        for n in range(len(state)):
            if (state[n] == 1):
                state[n]=(numpy.random.choice([0,1], p=[prob,(1-prob)]))
                if (state[n] == 0):
                    nb_is +=1
                    G.nodes[n]['visited'] = False
            if liste[n] == 1:
                state[n] = state[n] + liste[n]

        ### honeypots
        honeypot1 = honey_pot(G, nodes_out, nodes_in, resist, liste_edge, liste_resist, nbr, nbr_smart)
    

    ## début de la boucle avec installation d'antivirus 
    while (1 in state):
        liste = [0] * len(state)
        liste_edge = []
        liste_node = []
        nodes_out = []
        nodes_in = []

        nb_sr = Suscep_Resist(G, state, liste, alpha, resist, nb_sr) 
        liste_resist = resist_list(resist, state, G) 
        
        for n in G.nodes:  
            if (state[n]==1): 
                neighbors = liste_neighbors[G.nodes[n]['index']][:]
                suscep_neighbors = [v for v in neighbors if state[v] == 0]
                for t in suscep_neighbors:
                    if (not G.nodes[t]['visited'] and random.random()<p_inf):
                            G.nodes[t]['visited'] = True
                            edge_index = G[n][t]['index']
                            liste[t] = 1
                            if edge_index in honeypot1:
                                liste_edge.append(G[n][t]['index'])
                                liste_node.extend([n,t])
                                nodes_out.append(n)
                                nodes_in.append(t)                
        
        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                            
            G.nodes[i]['visited'] = False

        n_i = len([s for s in state if s == 1]) + len([l for l in liste if l==1])
        inf_nb.append(n_i)
        sr_bool = n_i >= seuil_sr

        for n in  range(len(state)):
            if (state[n]==1):
                state[n]=(numpy.random.choice([0,1], p=[prob,(1-prob)]))
                if (state[n]== 0):
                    nb_is +=1
                    G.nodes[n]['visited'] = False
            if liste[n]==1:
                state[n] = state[n] + liste[n]
                     
        ### honeypots
        honeypot1 = honey_pot(G, nodes_out, nodes_in, resist, liste_edge, liste_resist, nbr, nbr_smart)

   ### nombre cumulé d'infectés
    n_t = sum(inf_nb) 
    ep = np.max(inf_nb)

    return ep, n_t, nb_sr, nb_is
    

################################################################################################
# Retourne les aretes de liste_node qui ne sont pas résistantes                                #
# Inputs :                                                                                     #
# - G : graphe                                                                                 #
# - liste_node : liste des noeuds nouvellement défendus                                        #
# - liste_resist : liste des arêtes résistantes (liées à un noeud résistant)                   #
# Outputs :                                                                                    #
#  : arêtes non résistantes reliées aux noeuds défendus                                        #
################################################################################################
def edge_def(G, liste_node, liste_resist):
    edge_def =[]
    for i in liste_node:
        for j in list(G.neighbors(i)):
            index = G[i][j]['index']
            if ((index not in liste_resist) and (index not in edge_def)):
                edge_def.append(index)   
    return  edge_def


################################################################################################
# Calcul des nouveaux noeuds résistants (S -> R)                                               #
# Inputs :                                                                                     #
# - G : graphe                                                                                 #
# - state : liste des états de tous les  noeuds                                                #
# - liste : liste des états courants de tous les noeuds                                        #
# - alpha : probabilité de faire S -> R                                                        #
# - resist : liste des noeuds résistatns                                                       #
# Outputs :                                                                                    #
#  - liste des noeuds résistants mise à jour                                                   #
################################################################################################
def Suscep_Resist(G, state, liste, alpha, resist,nb_sr):
    nv_resist = []
    for n in G.nodes:
        if (state[n] == 0):
            liste[n] = (numpy.random.choice([-1,0], p=[alpha,(1-alpha)]))
            if (liste[n] == -1):
                nb_sr +=1
                G.nodes[n]['visited'] = True 
                nv_resist.append(n)  
    resist.extend(nv_resist) 
    return nb_sr


################################################################################################
# Mise à jour des états des noeuds infectés au départ                                          #
# Inputs :                                                                                     #
# - G : graphe                                                                                 #
# - state : liste des états de tous les  noeuds                                                #
# - begin : liste des noeuds infectés au départ                                                #
# Outputs :                                                                                    #
# - liste des états mise à jour                                                                #
################################################################################################
def begin_node(begin, state, G):
    for i in begin:  
        state[i] = 1
        G.nodes[i]['visited'] = True
    return state    


################################################################################################
# Met à jour les états des noeuds résistants et renvoie les arêtes résistantes                 #
# Inputs :                                                                                     #
# - G : graphe                                                                                 #
# - state : liste des états de tous les  noeuds                                                #
# - resist : liste des noeuds résistatns                                                       #
# Outputs :                                                                                    #
# - liste des états mise à jour et la liste des arêtes résistantes                             #
################################################################################################
### Traitement des noeuds résistants de départ + retour des index des aretes liant un sommet résistant et un de ses voisins
def resist_list(resist, state, G):
    list_edge = []
    for j in resist:
        state[j] = -1
        G.nodes[j]['visited'] = True
        list_edge.extend((G[j][i]['index'] for i in G.neighbors(j)))
    return list_edge


################################################################################################
# Mise en place des honeypots/IDS                                                              #
# Inputs :                                                                                     #
# - G : graphe                                                                                 #
# - nodes_out : noeuds qui ont tenté d'infecter au tour d'avant                                #
# - nodes_in : noeuds qui ont été infectés et défendus au tour d'avant                         #
# - resist : liste des noeuds résistatns                                                       #
# - list_edge : liste des arêtes attaquées au tour d'avant                                     #
# - liste_resit : liste des arêtes résistantes                                                 # 
# - nbr_honey : nombre de honeypots                                                            #
# - nbr_honey_smart : nombre de honeypots smarts                                               #
# - state : liste des états de tous les  noeuds                                                #
# Outputs :                                                                                    #
# - liste des arêtes où les honeypots ont été mis en place                                     #
################################################################################################
### Honey pot 
def honey_pot(G,nodes_out,nodes_in,resist,list_edge,liste_resist,nbr_honey,nbr_honey_smart):
    edge_total =[]
    len_smart = []
    neigh = []
    edge_smart = []
    
    ### neigh = liste de liste de voisins qui n'ont pas été attaqués ce tour et qui ne sont pas résistants
    for n in nodes_out :
        liste_remove = (list(G.neighbors(n)))
        for i in liste_remove:
            if ((i in resist) or (i in nodes_in)):
                liste_remove.remove(i)

        neigh.append(liste_remove)
        
    ### on calcule le nombre de voisins non résistants de chaque voisin et on ajoute une arete à visiter
    for k in range(len(neigh)):
        for i in range(len(neigh[k][:])):
            list_neigh = (list(G.neighbors(neigh[k][i])))
            for j in list_neigh:
                if j in resist:
                    list_neigh.remove(j)
            len_smart.append(len(list_neigh)) 
            edge_smart.append(G[neigh[k][i]][nodes_out[k]]['index'] )   
    
            
    for n in G.nodes():
        list_ne = (list(G.neighbors(n)))            
        for i in range(len(list_ne)):
            edge = G[list_ne[i]][n]['index']
            if ((edge not in list_edge) and (edge not in edge_smart) and (edge not in liste_resist) and (edge not in edge_total)):
                edge_total.append(edge)  

                
    taille = len(edge_total)
    tail_smart = len(edge_smart)
    borne = min(tail_smart, nbr_honey_smart)

    if (borne == 0): 
        hosp = random.sample(edge_total, k= min(nbr_honey, taille))
    else:
        honey_smart = random.choices(edge_smart,weights=len_smart,k=borne)
        hosp = random.sample(edge_total, k= min(nbr_honey-borne,taille))
        hosp.extend(honey_smart)

    return hosp         
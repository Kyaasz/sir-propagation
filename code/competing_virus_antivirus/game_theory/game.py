######################################################################
### Fichier de génération de la simulation sans l'aspect animation ###
######################################################################

import random
import numpy as np
import networkx as nx
import Delta_time_fun

################################################################################################
# Simule la propagation du virus avec la première dynamique de propagation : chaque noeud      #
# infecté transmet le virus à un de ses voisins susceptibles tiré aléatoirement                #
# Inputs :                                                                                     #
# - infected : liste des noeuds infectés au début de la simulation                             #
# - G : graphe                                                                                 #
# - alpha : proba de faire I -> S                                                              #
# - def_step : étape à laquelle l'antivirus est propagé                                        #
# - infection_probability : proba d'infecter un voisin                                         #
# - recovery_probability : proba de rétablir un voisin                                         #
# - K : cout investi dans la recherche d'un antivirus                                          #
################################################################################################


def unicast_competing_propagation(G, infected, alpha, infection_probability, recovery_probability, K):
    node_list = list(G.nodes)  
    neighbors_list = [list(G.neighbors(n)) for n in node_list] ### liste des listes de voisins
    states = [0]*G.number_of_nodes()
    
    # initialement, aucun sommet n'est infecté, immunisé
    nx.set_node_attributes(G, False, 'infected')
    nx.set_node_attributes(G, False, 'immune')
    ### Arêtes résistantes   
    immune_edges = [] 

    ### Mise à jour des états avec les infectés/résistants de base 
    for n in infected:
        G.nodes[n]['infected'] = True
        states[n] = 1

    inf_threshold = int(len(node_list)*0.05) ## seuil à 5% des noeuds
    inf_nb = len(infected)
    inf_tab = [inf_nb]
    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(inf_nb < inf_threshold): 
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        neighbor = random.choice(suscep_neighbors)
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ### Virus repéré, recherche d'un antivirus : 
    Delta = Delta_time_fun.delta_fun(K) # durée de la recherche de l'antivirus
    for k in range(Delta):
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        neighbor = random.choice(suscep_neighbors)
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ## Injection de l'antivirus
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []

    ### Propagation du virus et de l'antivirus
    while (1 in states): 
        edges_antivirus = [] ## arêtes par lesquelles passe l'antivirus
        random.shuffle(node_list) ## on mélange la liste pour ne pas toujours commencer par les mêmes noeuds
        for n in node_list:
            if ((G.nodes[n]['infected']) and (states[n] == 1)): ## cas où le noeud est infecté => le virus se propage
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    neighbor = random.choice(suscep_neighbors)
                    nb_alea = random.random()
                    if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
            if G.nodes[n]['immune']: ## cas où le noeud est immunisé => l'antivirus se propage
                candidates_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['immune'])]
                if len(candidates_neighbors) > 0: 
                    neighbor = random.choice(candidates_neighbors)
                    nb_alea = random.random()
                    if nb_alea < recovery_probability: ## on infecte
                        edges_antivirus.append(G[n][neighbor]['index'])
                        states[neighbor] = -1
                        immune_edges.extend([G[v][neighbor]['index'] for v in neighbors_list[G.nodes[neighbor]['index']]])
                        immune_edges = list(set(immune_edges))
                        immune_nodes.append(neighbor)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False
        step +=1

    return np.max(inf_tab), inf_tab
##############################################
# ########
######################################################

def broadcast_competing_propagation(G, infected, alpha, infection_probability, recovery_probability, K):
    node_list = list(G.nodes)  
    neighbors_list = [list(G.neighbors(n)) for n in node_list] ### liste des listes de voisins
    states = [0]*G.number_of_nodes()
    
    # initialement, aucun sommet n'est infecté, immunisé
    nx.set_node_attributes(G, False, 'infected')
    nx.set_node_attributes(G, False, 'immune')
    ### Arêtes résistantes   
    immune_edges = [] 

    ### Mise à jour des états avec les infectés/résistants de base 
    for n in infected:
        G.nodes[n]['infected'] = True
        states[n] = 1

    inf_threshold = int(len(node_list)*0.05) ## seuil à 5% des noeuds
    inf_nb = len(infected)
    inf_tab = [inf_nb]
    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(inf_nb < inf_threshold): 
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors:
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ### Virus repéré, recherche d'un antivirus : 
    Delta = Delta_time_fun.delta_fun(K) # durée de la recherche de l'antivirus
    for k in range(Delta):
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ## Injection de l'antivirus
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []

    ### Désormais on a également l'antivirus
    while (1 in states): 
        edges_antivirus = [] ## arêtes par lesquelles passe l'antivirus
        random.shuffle(node_list) ## on mélange la liste pour ne pas toujours commencer par les mêmes noeuds
        for n in node_list:
            if ((G.nodes[n]['infected']) and (states[n] == 1)): ## cas où le noeud est infecté => le virus se propage
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors: 
                    nb_alea = random.random()
                    if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
            if G.nodes[n]['immune']: ## cas où le noeud est immunisé => l'antivirus se propage
                candidates_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['immune'])]
                if len(candidates_neighbors) > 0: 
                    neighbor = random.choice(candidates_neighbors) 
                    nb_alea = random.random()
                    if nb_alea < recovery_probability: ## on infecte
                        edges_antivirus.append(G[n][neighbor]['index'])
                        states[neighbor] = -1
                        immune_edges.extend([G[v][neighbor]['index'] for v in neighbors_list[G.nodes[neighbor]['index']]])
                        immune_edges = list(set(immune_edges))
                        immune_nodes.append(neighbor)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False
        step +=1

    return np.max(inf_tab), inf_tab



    ##############################################
# ########
######################################################

def crazy_competing_propagation(G, infected, alpha, infection_probability, recovery_probability, K):
    node_list = list(G.nodes)  
    neighbors_list = [list(G.neighbors(n)) for n in node_list] ### liste des listes de voisins
    states = [0]*G.number_of_nodes()
    
    # initialement, aucun sommet n'est infecté, immunisé
    nx.set_node_attributes(G, False, 'infected')
    nx.set_node_attributes(G, False, 'immune')
    ### Arêtes résistantes   
    immune_edges = [] 

    ### Mise à jour des états avec les infectés/résistants de base 
    for n in infected:
        G.nodes[n]['infected'] = True
        states[n] = 1

    inf_threshold = int(len(node_list)*0.05) ## seuil à 5% des noeuds
    inf_nb = len(infected)
    inf_tab = [inf_nb]
    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(inf_nb < inf_threshold): 
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if random.random() < 1/2:
                    for neighbor in suscep_neighbors:
                        nb_alea = random.random()
                        if nb_alea < infection_probability : ## on infecte
                            states[neighbor] = 1
                else:
                    if len(suscep_neighbors) > 0: 
                        nb_alea = random.random()
                        if nb_alea < infection_probability : ## on infecte
                            neighbor = random.choice(suscep_neighbors)
                            states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ### Virus repéré, recherche d'un antivirus : 
    Delta = Delta_time_fun.delta_fun(K) # durée de la recherche de l'antivirus
    for k in range(Delta):
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if random.random() < 1/2:
                    for neighbor in suscep_neighbors:
                        nb_alea = random.random()
                        if nb_alea < infection_probability : ## on infecte
                            states[neighbor] = 1
                else:
                    if len(suscep_neighbors) > 0: 
                        nb_alea = random.random()
                        if nb_alea < infection_probability : ## on infecte
                            neighbor = random.choice(suscep_neighbors)
                            states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ## Injection de l'antivirus
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []

    ### Désormais on a également l'antivirus
    while (1 in states): 
        edges_antivirus = [] ## arêtes par lesquelles passe l'antivirus
        random.shuffle(node_list) ## on mélange la liste pour ne pas toujours commencer par les mêmes noeuds
        for n in node_list:
            if ((G.nodes[n]['infected']) and (states[n] == 1)): ## cas où le noeud est infecté => le virus se propage
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if random.random() < 1/2:
                    for neighbor in suscep_neighbors:
                        nb_alea = random.random()
                        if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                            states[neighbor] = 1
                else:
                    if len(suscep_neighbors) > 0: 
                        nb_alea = random.random()
                        if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                            neighbor = random.choice(suscep_neighbors)
                            states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
            if G.nodes[n]['immune']: ## cas où le noeud est immunisé => l'antivirus se propage
                candidates_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['immune'])]
                if len(candidates_neighbors) > 0: 
                    neighbor = random.choice(candidates_neighbors) 
                    nb_alea = random.random()
                    if nb_alea < recovery_probability: ## on infecte
                        edges_antivirus.append(G[n][neighbor]['index'])
                        states[neighbor] = -1
                        immune_edges.extend([G[v][neighbor]['index'] for v in neighbors_list[G.nodes[neighbor]['index']]])
                        immune_edges = list(set(immune_edges))
                        immune_nodes.append(neighbor)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False
        step +=1

    return np.max(inf_tab), inf_tab

##############################################################################
##############################################################################
##############################################################################


def sneaky_competing_propagation(G, infected, alpha, infection_probability, recovery_probability, K):
    node_list = list(G.nodes)  
    neighbors_list = [list(G.neighbors(n)) for n in node_list] ### liste des listes de voisins
    states = [0]*G.number_of_nodes()
    
    # initialement, aucun sommet n'est infecté, immunisé
    nx.set_node_attributes(G, False, 'infected')
    nx.set_node_attributes(G, False, 'immune')
    ### Arêtes résistantes   
    immune_edges = [] 

    ### Mise à jour des états avec les infectés/résistants de base 
    for n in infected:
        G.nodes[n]['infected'] = True
        states[n] = 1

    inf_threshold = int(len(node_list)*0.05) ## seuil à 5% des noeuds
    inf_nb = len(infected)
    inf_tab = [inf_nb]
    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(inf_nb < inf_threshold): 
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        neighbor = random.choice(suscep_neighbors)
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ### Virus repéré, recherche d'un antivirus : 
    Delta = Delta_time_fun.delta_fun(K) # durée de la recherche de l'antivirus
    for k in range(Delta):
        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        neighbor = random.choice(suscep_neighbors)
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        step +=1

    ## Injection de l'antivirus
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []

    ### Désormais on a également l'antivirus
    while (1 in states): 
        edges_antivirus = [] ## arêtes par lesquelles passe l'antivirus
        random.shuffle(node_list) ## on mélange la liste pour ne pas toujours commencer par les mêmes noeuds
        for n in node_list:
            if ((G.nodes[n]['infected']) and (states[n] == 1)): ## cas où le noeud est infecté => le virus se propage
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors:
                    nb_alea = random.random()
                    if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
            if G.nodes[n]['immune']: ## cas où le noeud est immunisé => l'antivirus se propage
                candidates_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['immune'])]
                if len(candidates_neighbors) > 0: 
                    neighbor = random.choice(candidates_neighbors) 
                    nb_alea = random.random()
                    if nb_alea < recovery_probability: ## on infecte
                        edges_antivirus.append(G[n][neighbor]['index'])
                        states[neighbor] = -1
                        immune_edges.extend([G[v][neighbor]['index'] for v in neighbors_list[G.nodes[neighbor]['index']]])
                        immune_edges = list(set(immune_edges))
                        immune_nodes.append(neighbor)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        inf_nb = len(temp)
        inf_tab.append(inf_nb)
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False
        step +=1

    return np.max(inf_tab), inf_tab
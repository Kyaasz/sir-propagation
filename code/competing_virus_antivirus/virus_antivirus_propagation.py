################################################################
### Fichier de génération de simulation - virus et antivirus ###
################################################################

import random
import numpy as np
import networkx as nx

################################################################################################
# Simule la propagation du virus avec la première dynamique de propagation : chaque noeud      #
# infecté transmet le virus à un de ses voisins susceptibles tiré aléatoirement                #
# Inputs :                                                                                     #
# - infected : liste des noeuds infectés au début de la simulation                             #
# - G : graphe                                                                                 #
# - q : queue pour l'animation                                                                 #
# - alpha : proba de faire I -> S                                                              #
# - def_step : étape à laquelle l'antivirus est propagé                                        #
# - infection_probability : proba d'infecter un voisin                                         #
# - recovery_probability : proba de rétablir un voisin                                         #
################################################################################################


def unicast_competing_propagation(G, infected, alpha, def_step, infection_probability, recovery_probability, q):
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
    
    q.update_infected(infected)
    q.state_step(states)

    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(step < def_step): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []

        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        neighbor = random.choice(suscep_neighbors)
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[neighbor][n]['index'])
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR
                if states[n]==0:
                    recovered_nodes.append(n)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.state_step(states)

        step +=1
        
    ### Fin de la première boucle

    ## On injecte l'antivirus dans un noeud
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []
    q.update_immune([imm], immune_edges)

    ### Désormais on a également l'antivirus
    while (1 in states): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []
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
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[n][neighbor]['index'])
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
                if states[n]==0:
                    recovered_nodes.append(n)
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
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.update_immune_edges(edges_antivirus)
        q.update_immune(immune_nodes, immune_edges)
        q.state_step(states)
        
        step +=1
    


################################################################################################
# Simule la propagation du virus avec la première dynamique de propagation : chaque noeud      #
# infecté transmet le virus à tous ses voisins susceptibles tiré aléatoirement                 #
# Inputs :                                                                                     #
# - infected : liste des noeuds infectés au début de la simulation                             #
# - G : graphe                                                                                 #
# - q : queue pour l'animation                                                                 #
# - alpha : proba de faire I -> S                                                              #
# - def_step : étape à laquelle l'antivirus est propagé                                        #
# - infection_probability : proba d'infecter un voisin                                         #
# - recovery_probability : proba de rétablir un voisin                                         #
################################################################################################


def broadcast_competing_propagation(G, infected, alpha, def_step, infection_probability, recovery_probability, q):
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
    
    q.update_infected(infected)
    q.state_step(states)

    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(step < def_step): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []

        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[neighbor][n]['index'])
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR
                if states[n]==0:
                    recovered_nodes.append(n)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.state_step(states)

        step +=1
        
    ### Fin de la première boucle

    ## On injecte l'antivirus dans un noeud
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []
    q.update_immune([imm], immune_edges)

    ### Désormais on a également l'antivirus
    while (1 in states): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []
        edges_antivirus = [] ## arêtes par lesquelles passe l'antivirus
        random.shuffle(node_list) ## on mélange la liste pour ne pas toujours commencer par les mêmes noeuds
        for n in node_list:
            if ((G.nodes[n]['infected']) and (states[n] == 1)): ## cas où le noeud est infecté => le virus se propage
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors: 
                    nb_alea = random.random()
                    if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                        states[neighbor] = 1
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[n][neighbor]['index'])
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
                if states[n]==0:
                    recovered_nodes.append(n)
            if G.nodes[n]['immune']: ## cas où le noeud est immunisé => l'antivirus se propage
                candidates_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['immune'])]
                for neighbor in candidates_neighbors: 
                    nb_alea = random.random()
                    if nb_alea < recovery_probability: ## on infecte
                        edges_antivirus.append(G[n][neighbor]['index'])
                        states[neighbor] = -1
                        immune_edges.extend([G[v][neighbor]['index'] for v in neighbors_list[G.nodes[neighbor]['index']]])
                        immune_edges = list(set(immune_edges))
                        immune_nodes.append(neighbor)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.update_immune_edges(edges_antivirus)
        q.update_immune(immune_nodes, immune_edges)
        q.state_step(states)
        
        step +=1

###########################################################



def unicast_competing_contagious_propagation(G, infected, alpha, def_step, infection_probability, recovery_probability, q):
    node_list = list(G.nodes)  
    neighbors_list = [list(G.neighbors(n)) for n in node_list] ### liste des listes de voisins
    states = [0]*G.number_of_nodes()
    # initialement, aucun sommet n'est infecté, immunisé
    nx.set_node_attributes(G, False, 'infected')
    nx.set_node_attributes(G, False, 'immune')
    nx.set_node_attributes(G, False, 'contagious')
    ### Arêtes résistantes   
    immune_edges = [] 

    ### Mise à jour des états avec les infectés/résistants de base 
    for n in infected:
        G.nodes[n]['infected'] = True
        G.nodes[n]['contagious'] = True
        states[n] = 1

    q.update_infected(infected)
    q.update_contagious(infected)
    q.state_step(states)

    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    to_become_contagious = []
    while(step < def_step): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []
        contagious_list = []
        for n in node_list:
            if G.nodes[n]['contagious']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        neighbor = random.choice(suscep_neighbors)
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[neighbor][n]['index'])
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR
                if states[n]==0:
                    recovered_nodes.append(n)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        for n in temp:
            G.nodes[n]['infected'] = True
            if n in to_become_contagious:
                G.nodes[n]['contagious'] = True
                to_become_contagious.remove(n)
                contagious_list.append(n)
            to_become_contagious.append(n)
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
            G.nodes[n]['contagious'] = False
            if n in to_become_contagious:
                to_become_contagious.remove(n)

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.update_contagious(contagious_list)
        q.state_step(states)

        step +=1
        
    ### Fin de la première boucle

    ## On injecte l'antivirus dans un noeud
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    G.nodes[imm]['contagious'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []
    q.update_immune([imm], immune_edges)

    ### Désormais on a également l'antivirus
    while (1 in states): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []
        edges_antivirus = [] ## arêtes par lesquelles passe l'antivirus
        contagious_list = []
        random.shuffle(node_list) ## on mélange la liste pour ne pas toujours commencer par les mêmes noeuds
        for n in node_list:
            if ((G.nodes[n]['contagious']) and (states[n] == 1)): ## cas où le noeud est infecté => le virus se propage
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    neighbor = random.choice(suscep_neighbors)
                    nb_alea = random.random()
                    if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                        states[neighbor] = 1
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[n][neighbor]['index'])
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
                if states[n]==0:
                    recovered_nodes.append(n)
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
        for n in temp:
            G.nodes[n]['infected'] = True
            if n in to_become_contagious:
                G.nodes[n]['contagious'] = True
                to_become_contagious.remove(n)
                contagious_list.append(n)
            to_become_contagious.append(n)
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
            G.nodes[n]['contagious'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False
            G.nodes[n]['contagious'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.update_immune_edges(edges_antivirus)
        q.update_immune(immune_nodes, immune_edges)
        q.update_contagious(contagious_list)
        q.state_step(states)
        
        step +=1

        
    

def unicast_virus_competing_propagation(G, infected, alpha, def_step, infection_probability, recovery_probability, q):
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
    
    q.update_infected(infected)
    q.state_step(states)

    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(step < def_step): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []

        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                if len(suscep_neighbors) > 0: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        neighbor = random.choice(suscep_neighbors)
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[neighbor][n]['index'])
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR
                if states[n]==0:
                    recovered_nodes.append(n)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.state_step(states)

        step +=1
        
    ### Fin de la première boucle

    ## On injecte l'antivirus dans un noeud
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []
    q.update_immune([imm], immune_edges)

    ### Désormais on a également l'antivirus
    while (1 in states): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []
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
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[n][neighbor]['index'])
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
                if states[n]==0:
                    recovered_nodes.append(n)
            if G.nodes[n]['immune']: ## cas où le noeud est immunisé => l'antivirus se propage
                candidates_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['immune'])]
                for neighbor in candidates_neighbors: 
                    nb_alea = random.random()
                    if nb_alea < recovery_probability: ## on infecte
                        edges_antivirus.append(G[n][neighbor]['index'])
                        states[neighbor] = -1
                        immune_edges.extend([G[v][neighbor]['index'] for v in neighbors_list[G.nodes[neighbor]['index']]])
                        immune_edges = list(set(immune_edges))
                        immune_nodes.append(neighbor)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.update_immune_edges(edges_antivirus)
        q.update_immune(immune_nodes, immune_edges)
        q.state_step(states)
        
        step +=1




def unicast_antivirus_competing_propagation(G, infected, alpha, def_step, infection_probability, recovery_probability, q):
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
    
    q.update_infected(infected)
    q.state_step(states)

    step = 0
    ### première phase où l'antivirus n'est pas encore déployé
    ## Dans chaque tour de boucle, tous les noeuds infectés vont pouvoir infecter un de leurs voisins susceptibles avec probabilité infection_probability
    while(step < def_step): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []

        for n in node_list:
            if G.nodes[n]['infected']: 
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors: 
                    nb_alea = random.random()
                    if nb_alea < infection_probability : ## on infecte
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[neighbor][n]['index'])
                        states[neighbor] = 1
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guériR
                if states[n]==0:
                    recovered_nodes.append(n)

        ### mise à jour des états des noeuds
        temp = [n for n in range(len(states)) if states[n] == 1]
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.state_step(states)

        step +=1
        
    ### Fin de la première boucle

    ## On injecte l'antivirus dans un noeud
    imm = random.choice(node_list)
    G.nodes[imm]['immune'] = True
    G.nodes[imm]['infected'] = False
    states[imm] = -1
    immune_edges.extend([G[imm][v]['index'] for v in neighbors_list[G.nodes[imm]['index']]])
    immune_edges = list(set(immune_edges))
    immune_nodes = []
    q.update_immune([imm], immune_edges)

    ### Désormais on a également l'antivirus
    while (1 in states): 
        infected_nodes = []
        infected_edges = []
        recovered_nodes = []
        edges_antivirus = [] ## arêtes par lesquelles passe l'antivirus
        random.shuffle(node_list) ## on mélange la liste pour ne pas toujours commencer par les mêmes noeuds
        for n in node_list:
            if ((G.nodes[n]['infected']) and (states[n] == 1)): ## cas où le noeud est infecté => le virus se propage
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['infected'] or G.nodes[v]['immune'])]
                for neighbor in suscep_neighbors: 
                    nb_alea = random.random()
                    if ((nb_alea < infection_probability) and (states[neighbor] == 0)): ## on infecte
                        states[neighbor] = 1
                        infected_nodes.append(neighbor)
                        infected_edges.append(G[n][neighbor]['index'])
                states[n] = np.random.choice([0, 1], p=[alpha, 1-alpha]) ## le noeud peut potentiellement guérir
                if states[n]==0:
                    recovered_nodes.append(n)
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
        for n in temp:
            G.nodes[n]['infected'] = True
        temp = [n for n in range(len(states)) if states[n] == 0]
        for n in temp:
            G.nodes[n]['infected'] = False
        temp = [n for n in range(len(states)) if states[n] == -1]
        for n in temp:
            G.nodes[n]['immune'] = True
            G.nodes[n]['infected'] = False

        q.update_infected_edges(infected_edges)
        q.update_infected(infected_nodes)
        q.inv_update_infected_edges(infected_edges)
        q.update_recovered(recovered_nodes)
        q.update_immune_edges(edges_antivirus)
        q.update_immune(immune_nodes, immune_edges)
        q.state_step(states)
        
        step +=1
#####################################################################
### Fichier qui génère les simulations pour les virus concurrents ###
#####################################################################

import random
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


def unicast_simple_competing_propagation(G, infected_a, infected_b, infection_probability_a, infection_probability_b, q):
    node_list = list(G.nodes)  
    neighbors_list = [list(G.neighbors(n)) for n in node_list] ### liste des listes de voisins
    states = [0]*G.number_of_nodes() ### 0 <=> aucune affectation, 1 <=> contaminé par A, -1 <=> contaminé par B
    # initialement, aucun sommet n'est infecté, immunisé
    nx.set_node_attributes(G, False, 'A-infected')
    nx.set_node_attributes(G, False, 'B-infected')

    ### Mise à jour des états avec les infectés de base 
    for n in infected_a:
        G.nodes[n]['A-infected'] = True
        states[n] = 1
    
    for n in infected_b:
        G.nodes[n]['B-infected'] = True
        states[n] = -1
    
    q.update_infected_a_nodes(infected_a)
    q.update_infected_b_nodes(infected_b)
    q.state_step(states)

    step = 0
    flag = -1
    max_iter = 10000
    ### BOUCLE PRINCIPALE
    while flag<0: 
        print("step", step)
        random.shuffle(node_list)
        a_infected_edges = []
        a_infected_nodes = []
        b_infected_edges = []
        b_infected_nodes = []

        # on boucle sur l'ensemble des noeuds
        for n in node_list: 
            if (G.nodes[n]['A-infected'] and states[n] == 1):
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['A-infected'])]
                if len(suscep_neighbors)>0:
                    neighbor = random.choice(suscep_neighbors)
                    if (not(states[neighbor] == -1 and not(G.nodes[neighbor]['B-infected']))) :
                        if (random.random() < infection_probability_a and states[neighbor] == 0) or (random.random() < (infection_probability_a/2) and states[neighbor] == -1):
                            states[neighbor] = 1
                            a_infected_nodes.append(neighbor)
                            a_infected_edges.append(G[n][neighbor]['index'])
            elif (G.nodes[n]['B-infected'] and states[n] == -1):
                suscep_neighbors = [v for v in neighbors_list[G.nodes[n]['index']] if not(G.nodes[v]['B-infected'])]
                if len(suscep_neighbors)>0:
                    neighbor = random.choice(suscep_neighbors)
                    if (not(states[neighbor] == 1 and not(G.nodes[neighbor]['A-infected']))) :
                        if (states[neighbor] == 0 and random.random() < infection_probability_b) or (states[neighbor] == 1 and random.random()<(infection_probability_b/2)):
                            states[neighbor] = -1
                            b_infected_nodes.append(neighbor)
                            b_infected_edges.append(G[n][neighbor]['index'])
            
        # maj des états
        for n in a_infected_nodes:
            G.nodes[n]['A-infected'] = True
            G.nodes[n]['B-infected'] = False
        
        for n in b_infected_nodes:
            G.nodes[n]['B-infected'] = True
            G.nodes[n]['A-infected'] = False

        # animation
        q.update_infected_a_edges(a_infected_edges)
        q.update_infected_b_edges(b_infected_edges)
        q.update_infected_a_nodes(a_infected_nodes)
        q.update_infected_b_nodes(b_infected_nodes)
        a_infected_edges.extend(b_infected_edges)
        q.inv_update_infected_edges(a_infected_edges)
        q.state_step(states)

        step += 1 
        # conditions de fin 
        if not(1 in states):
            flag = 1
        elif not(-1 in states):
            flag =2
        elif(step > max_iter):
            flag = 0
    
    match flag:
        case 0:
            print("Nombre d'itérations maximal atteint")
        case 1:
            print("Consensus B")
        case 2: 
            print("Consensus A")
        case _:
            pass


def neighborhood_competing_propagation(G, infected_a, infected_b, infection_probability_a, infection_probability_b, q):
    node_list = list(G.nodes)  
    neighbors_list = [list(G.neighbors(n)) for n in node_list] ### liste des listes de voisins
    states = [0]*G.number_of_nodes() ### 0 <=> aucune affectation, 1 <=> contaminé par A, -1 <=> contaminé par B
    # initialement, aucun sommet n'est infecté, immunisé
    nx.set_node_attributes(G, False, 'A-infected')
    nx.set_node_attributes(G, False, 'B-infected')

    ### Mise à jour des états avec les infectés de base 
    for n in infected_a:
        G.nodes[n]['A-infected'] = True
        states[n] = 1
    
    for n in infected_b:
        G.nodes[n]['B-infected'] = True
        states[n] = -1
    
    q.update_infected_a_nodes(infected_a)
    q.update_infected_b_nodes(infected_b)
    q.state_step(states)

    step = 0
    flag = -1
    max_iter = 500
    ### BOUCLE PRINCIPALE
    while flag<0: 
        print("step", step)
        random.shuffle(node_list)
        a_infected_edges = []
        a_infected_nodes = []
        b_infected_edges = []
        b_infected_nodes = []
        current_state = [0]*G.number_of_nodes()
        # on boucle sur l'ensemble des noeuds
        for n in node_list: 
            for k in neighbors_list[n]:
                if G.nodes[k]['A-infected']:
                    current_state[n] += 1
                elif G.nodes[k]['B-infected']:
                    current_state[n] -= 1
                if current_state[n] > 0: 
                    if states[n] != 1:
                        a_infected_nodes.append(n)
                    states[n] = 1
                elif current_state[n] < 0:
                    if current_state[n] != -1:
                        b_infected_nodes.append(n)
                    states[n] = -1
                else: 
                    states[n] = 0
        
        # maj des états
        for n in a_infected_nodes:
            G.nodes[n]['A-infected'] = True
            G.nodes[n]['B-infected'] = False
        
        for n in b_infected_nodes:
            G.nodes[n]['B-infected'] = True
            G.nodes[n]['A-infected'] = False

        # animation
        q.update_infected_a_edges([])
        q.update_infected_b_edges([])
        q.update_infected_a_nodes(a_infected_nodes)
        q.update_infected_b_nodes(b_infected_nodes)
        q.inv_update_infected_edges([])
        q.state_step(states)

        step += 1 
        # conditions de fin 
        if not(1 in states):
            flag = 1
        elif not(-1 in states):
            flag =2
        elif(step > max_iter):
            flag = 0
    
    match flag:
        case 0:
            print("Nombre d'itérations maximal atteint")
        case 1:
            print("Consensus B")
        case 2: 
            print("Consensus A")
        case _:
            pass
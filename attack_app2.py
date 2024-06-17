from calendar import c
import math
import random
from re import U
import matplotlib.pyplot as plt
import numpy
import networkx as nx


def propagation_unicast(begin, G, q, resist, alpha, prob, nbr, nbr_smart):
        
    state = [0] * G.number_of_nodes() ### Tous les noeuds sont initialement susceptibles
    liste_neighbors = [list(G.neighbors(n)) for n in G.nodes] ### liste des listes de voisins
    # initialement, aucun sommet n'a été visité/traité
    nx.set_node_attributes(G, False, 'visited')
                
    ### Mise à jour des états avec les infectés de base 
    state = begin_node(begin, state, G)
    q.push(state)

    ### Arêtes résistantes   
    liste_resist = resist_list(resist, state, G)

    # on ajoute les honeypot à traiter
    honeypot1 = honey_pot(G,[],[],resist,[],liste_resist,nbr,0)

    ### pour l'animation
    q.push_resist(state, liste_resist, honeypot1)
    q.hospot_anime(honeypot1)
    q.step_state(state)
    
    ### boucle principale
    while any(x in state for x in (0, 1)):  
        ### setup   
        liste = [0] * len(state)
        liste_SR = [0] * len(state)
        edges = [] ### arêtes traitées
        
        ### setup honeypots
        liste_edge = [] ### arêtes défendues
        liste_node  = [] ### noeuds défendus
        nodes_out = []
        nodes_in = []

        ### S -> R

        ### maj des noeuds résistants
        Suscep_Resist(G, state, liste, alpha, resist) 
        ### maj des arêtes résistantes
        liste_resist = resist_list(resist, state, G)

        ### PHASE D'ATTAQUE
        for n in G.nodes:  
            if (state[n] == 1): ### on ne traite que les noeuds infectés
                ### infection d'un voisin tiré aléatoirement
                index = G.nodes[n]['index']
                liste_suscep = [v for v in (liste_neighbors[index]) if state[v] == 0]
                if (len(liste_suscep) > 0):
                    t = random.choice(liste_suscep)
                    if not G.nodes[t]['visited']:
                        G.nodes[t]['visited'] = True
                        edge_index = G[t][n]['index']
                        edges.append(edge_index)
                        liste[t] = 1
                        ### l'arête où passe l'attaque était défendue
                        if edge_index in honeypot1:
                            liste_edge.append(edge_index)
                            nodes_out.append(n)
                            nodes_in.append(t)
                            liste_node.extend([n,t])                                        
                            for k in liste_node:
                                liste_SR[k] = 1             
                                            

        ### nouvelles arêtes résistantes            
        edge_def1 = edge_def(G, liste_node, liste_resist)

        ### pour l'animation
        q.push_resist(liste,liste_resist,honeypot1)
        q.push_edges(edges,honeypot1) #changer la couleur des edges en rouge 
        q.push(liste) #changer la couleur des nodes en rouge 
        q.push_defence(liste_SR,liste_edge,edge_def1,honeypot1) #pour les nodes défendus
        q.push_inv_edges(edges,honeypot1) #pour les edges rouges         
        
        ### Les noeuds ont été défendus, ils deviennent alors susceptibles
        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                                
            G.nodes[i]['visited'] = False
        
        ### PHASE DE GUERISON
        node_IS = []
        for n in G.nodes:
            if (state[n] == 1):
                state[n] = (numpy.random.choice([0,1], p=[prob, (1-prob)]))
                if (state[n] == 0):
                    G.nodes[n]['visited'] = False 
                    node_IS.append(n)
            if liste[n]==1:
                state[n] = state[n] + liste[n]
        
        edge_IS = edge_def(G, node_IS, liste_resist)
        q.push_IS(node_IS, edge_IS, honeypot1)

        

        ### pour l'animation
        q.new_attack(liste)
        q.step_state(state)
        q.suscep_resist(honeypot1,liste_resist)

        ### déplacement des ids/honeypots
        honeypot1 = honey_pot(G,nodes_out,nodes_in,resist,liste_edge,liste_resist,nbr,nbr_smart)

        q.hospot_anime(honeypot1)


def propagation_probability(begin,G,q,resist,alpha,prob,nbr,P,nbr_smart):
       
    state = [0] * G.number_of_nodes() ### Tous les noeuds sont initialement susceptibles
    liste_neighbors = [list(G.neighbors(n)) for n in G.nodes] ### liste des listes de voisins

    # initialement, aucun sommet n'a été visité/traité
    nx.set_node_attributes(G, False, 'visited')
                
    ### Mise à jour des états avec les infectés de base 
    state = begin_node(begin, state, G)
    q.push(state)

    ### Arêtes résistantes   
    liste_resist = resist_list(resist, state, G)

    # on ajoute les honeypot à traiter
    honeypot1 = honey_pot(G,[],[],resist,[],liste_resist,nbr,0)

    ### pour l'animation
    q.push_resist(state, liste_resist, honeypot1)
    q.hospot_anime(honeypot1)
    q.step_function(1) 
    q.step_state(state)
    
    
    while any(x in state for x in (0, 1)): 
        liste = [0] * len(state)
        liste_SR = [0] * len(state)
        edges = []
        liste_edge = []
        liste_node  = []
        nodes_out = []
        nodes_in = []
        
        Suscep_Resist(G, state, liste, alpha, resist) 
        liste_resist = resist_list(resist, state, G) 
        
        for n in G.nodes:  
            if (state[n]==1): 
                neighbors = liste_neighbors[G.nodes[n]['index']][:]
                suscep_neighbors = [v for v in neighbors if state[v] == 0]
                nb_attack = math.ceil(len(suscep_neighbors)*P)
                liste_random = random.sample(suscep_neighbors, k=nb_attack)
                                        
                for j in liste_random:
                    if not G.nodes[j]['visited']:
                        G.nodes[j]['visited'] = True
                        edge_index = G[n][j]['index']
                        edges.append(edge_index)
                        liste[j] = 1
                        if edge_index in honeypot1:
                            liste_edge.append(edge_index)
                            nodes_out.append(n)
                            nodes_in.append(j)
                            liste_node.extend([n,j])                  
                            for k in liste_node:
                                liste_SR[k] = 1 


        edge_def1 = edge_def(G,liste_node,liste_resist)

        ### animation 
        q.push_resist(liste,liste_resist,honeypot1)
        q.push_edges(edges,honeypot1) #changer le couleur de edge en rouge 
        q.push(liste) #changer le couleur des node en rouge 
        q.push_defence(liste_SR,liste_edge,edge_def1,honeypot1)#pour les node defence 
        q.push_inv_edges(edges,honeypot1)#pour les edge rouge         
        
        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                          
            G.nodes[i]['visited'] = False
            
        node_IS = []
        for n in G.nodes:
            if (state[n]==1):
                state[n]=(numpy.random.choice([0,1], p=[prob,(1-prob)]))
                if (state[n]== 0):
                    G.nodes[n]['visited'] = False
                    node_IS.append(n)
            if liste[n]==1:
                state[n] = state[n] + liste[n] 
        
        edge_IS = edge_def(G,node_IS,liste_resist)
        q.push_IS(node_IS,edge_IS,honeypot1)
          
        
        ### animation
        q.new_attack(liste)
        q.step_state(state)
        q.suscep_resist(honeypot1,liste_resist)

        honeypot1 = honey_pot(G,nodes_out,nodes_in,resist,liste_edge,liste_resist,nbr,nbr_smart)
        q.hospot_anime(honeypot1)


def propagation_broadcast(begin,G,q,resist,alpha,prob,nbr,nbr_smart):
        
    state = [0] * G.number_of_nodes() ### Tous les noeuds sont initialement susceptibles
    liste_neighbors = [list(G.neighbors(n)) for n in G.nodes] ### liste des listes de voisins

    # initialement, aucun sommet n'a été visité/traité
    nx.set_node_attributes(G, False, 'visited')
                
    ### Mise à jour des états avec les infectés de base 
    state = begin_node(begin, state, G)
    q.push(state)

    ### Arêtes résistantes   
    liste_resist = resist_list(resist, state, G)

    # on ajoute les honeypot à traiter
    honeypot1 = honey_pot(G,[],[],resist,[],liste_resist,nbr,0)

    ### pour l'animation
    q.push_resist(state, liste_resist, honeypot1)
    q.hospot_anime(honeypot1)
    q.step_function(1) 
    q.step_state(state)
    
    while any(x in state for x in (0, 1)):

        liste = liste = [0] * len(state)
        liste_SR = [0] * len(state)
        edges = []
        liste_edge =[]
        liste_node  =[]
        nodes_out=[]
        nodes_in=[]

        Suscep_Resist(G,state,liste,alpha,resist) 
        liste_resist = resist_list(resist,state,G) 
        
        for n in G.nodes:  
            if (state[n]==1): 
                neighbors = liste_neighbors[G.nodes[n]['index']][:]
                suscep_neighbors = [v for v in neighbors if state[v] == 0]
                for t in suscep_neighbors:
                    if not G.nodes[t]['visited']:
                            G.nodes[t]['visited'] = True
                            edge_index = G[n][t]['index']
                            edges.append(edge_index)
                            liste[t] = 1
                            if edge_index in honeypot1:
                                liste_edge.append(G[n][t]['index'])
                                liste_node.extend([n,t])
                                nodes_out.append(n)
                                nodes_in.append(t)
                                for j in liste_node:
                                    liste_SR[j] = 1             


        edge_def1=edge_def(G,liste_node,liste_resist) 

        ### animation
        q.push_resist(liste,liste_resist,honeypot1)
        q.push_edges(edges,honeypot1) #changer le couleur de edge en rouge 
        q.push(liste) #changer le couleur des node en rouge 
        q.push_defence(liste_SR,liste_edge,edge_def1,honeypot1)#pour les node defence 
        q.push_inv_edges(edges,honeypot1)#pour les edge rouge         
        
        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                            
            G.nodes[i]['visited'] = False
        
        
        node_IS = []
        for n in  range(len(state)):
            if (state[n]==1):
                state[n]=(numpy.random.choice([0,1], p=[prob,(1-prob)]))
                if (state[n]== 0):
                    G.nodes[n]['visited'] = False
                    node_IS.append(n)
            if liste[n]==1:
                state[n] = state[n] + liste[n]
          
        edge_IS = edge_def(G,node_IS,liste_resist)
        q.push_IS(node_IS,edge_IS,honeypot1) 
            
        ### animation
        q.new_attack(liste)
        q.step_state(state) 
        q.suscep_resist(honeypot1,liste_resist)

        ### honeypots
        honeypot1 = honey_pot(G,nodes_out,nodes_in,resist,liste_edge,liste_resist,nbr,nbr_smart)
        q.hospot_anime(honeypot1)

                
def propagation_deterministic_smart(begin,G,q,resist,alpha,prob,nbr,nbr_smart):                
          
       
    state = [0] * G.number_of_nodes() ### Tous les noeuds sont initialement susceptibles
    liste_neighbors = [list(G.neighbors(n)) for n in G.nodes] ### liste des listes de voisins

    # initialement, aucun sommet n'a été visité/traité
    nx.set_node_attributes(G, False, 'visited')
    
    state = begin_node(begin,state,G)
    q.push(state)
    
    liste_resist = resist_list(resist,state,G)
    honeypot1 = honey_pot(G,[],[],resist,[],liste_resist,nbr,0)
    
    q.push_resist(state,liste_resist,honeypot1)
    q.hospot_anime(honeypot1)
    q.step_function(1) 
    q.step_state(state)
    
    
    while any(x in state for x in (0, 1)):
        print("nouveau tour")
        liste = [0] * len(state)
        liste_SR = [0] * len(state)
        edges = []
        liste_edge = []
        liste_node  = []
        nodes_out = []
        nodes_in = []


        ### PHASE DE RESISTANCE
        Suscep_Resist(G,state,liste,alpha,resist) 
        liste_resist = resist_list(resist,state,G) 
        
        ### PHASE D'ATTAQUE
        for n in G.nodes:
            if (state[n] == 1):
                neighbors = liste_neighbors[G.nodes[n]['index']][:]
                list1 = []
                table_neigh = []
                liste_node_max = []
                ### voisins susceptibles
                for j in neighbors:
                    if (state[j] == 0):
                        list1.append(j)
                ### nombre de voisins des voisins
                for i in list1:
                    list_smart = []
                    for j in (list(G.neighbors(i))):
                        if (state[j] == 0):           
                            list_smart.append(j)
                    table_neigh.append(len(list_smart))
                if (len(table_neigh) > 0):
                    maxi = max(table_neigh) 
                else: 
                    maxi = 0
                ### voisins de degré maximal
                for m in range(len(table_neigh)):
                    if table_neigh[m] == maxi:
                        liste_node_max.append(list1[m])
                
                if (len(liste_node_max)!=0):
                    t = random.choice(liste_node_max) 

                    if not G.nodes[t]['visited']:
                        G.nodes[t]['visited'] = True
                        edge_index = G[n][t]['index']
                        edges.append(edge_index)
                        liste[t] = 1 
                        if edge_index in honeypot1:
                            liste_edge.append(edge_index)
                            liste_node.extend([n,t])
                            nodes_out.append(n)
                            nodes_in.append(t)
                            for j in liste_node:
                                liste_SR[j] = 1             
            
        
            
        edge_def1=edge_def(G,liste_node,liste_resist) 
        q.push_resist(liste,liste_resist,honeypot1)
        q.push_edges(edges,honeypot1) #changer le couleur de edge en rouge 
        q.push(liste) #changer le couleur des node en rouge 
        q.push_defence(liste_SR,liste_edge,edge_def1,honeypot1)#pour les node defence 
        q.push_inv_edges(edges,honeypot1)#pour les edge rouge         
        
        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                          
            G.nodes[i]['visited'] = False
        

        node_IS = []
        for i in range(len(state)):
            if (state[i]==1):
                state[i]=(numpy.random.choice([0,1], p=[prob,(1-prob)]))
                if (state[i]== 0):
                    G.nodes[i]['visited'] = False
                    node_IS.append(i)
            if liste[i]==1:
                state[i] = state[i] + liste[i] 
           

        edge_IS = edge_def(G,node_IS,liste_resist)
        q.push_IS(node_IS,edge_IS,honeypot1)   
        
        q.new_attack(liste)
        q.step_state(state) 
        q.suscep_resist(honeypot1,liste_resist)

        honeypot1 = honey_pot(G,nodes_out,nodes_in,resist,liste_edge,liste_resist,nbr,nbr_smart)
        q.hospot_anime(honeypot1)          

                
def propagation_probabilistic_smart(begin, G, q, resist, alpha, prob, nbr, nbr_smart):
       
    state = [0] * G.number_of_nodes() ### Tous les noeuds sont initialement susceptibles
    liste_neighbors = [list(G.neighbors(n)) for n in G.nodes] ### liste des listes de voisins

    # initialement, aucun sommet n'a été visité/traité
    nx.set_node_attributes(G, False, 'visited')
    
    state = begin_node(begin,state,G)
    q.push(state)
    
    liste_resist = resist_list(resist,state,G)
    honeypot1 = honey_pot(G,[],[],resist,[],liste_resist,nbr,0)
    
    q.push_resist(state,liste_resist,honeypot1)
    q.hospot_anime(honeypot1)
    q.step_function(1) 
    q.step_state(state)
    
    
    while any(x in state for x in (0, 1)):
        
        liste = [0] * len(state)
        liste_SR = [0] * len(state)
        edges = []

        liste_edge = []
        liste_node = []
        nodes_out = []
        nodes_in = []
        

        Suscep_Resist(G,state,liste,alpha,resist) 
        liste_resist = resist_list(resist,state,G) 
        
        
        for n in G.nodes:
            if (state[n]==1):
                neighbors = liste_neighbors[G.nodes[n]['index']][:]
                list1 = []
                table_neigh =[]
                liste_node_max = []
                neigh_not_max = []
                table_neigh_max = []
                list_not_max  = []
                liste2 = []
                ### voisins non résistants
                for j in neighbors:
                    if j  not in resist:
                        list1.append(j)
                ### nombre de voisins des voisins
                for i in list1:
                    list_smart= []
                    for j in (list(G.neighbors(i))):
                        if j  not in resist:           
                            list_smart.append(j)
                    table_neigh.append(len(list_smart))
                
                if (len(table_neigh) > 0):
                    maxi = max(table_neigh) 
                else: 
                    maxi = 0
                ### une liste de noeuds de degré maximal et une autre avec le reste
                for i in range(len(table_neigh)):
                    if table_neigh[i]==maxi:
                        liste_node_max.append(list1[i])
                    else:
                        list_not_max.append(list1[i])

                ### nombre de voisins non resistants des voisins de degré non maximal 
                for i in list_not_max:
                    for j in (list(G.neighbors(i))):
                        if j not in resist:           
                            neigh_not_max.append(j)
                    table_neigh_max.append(len(neigh_not_max))

                ## nombre aléatoire de noeuds non max        
                nbr_not = random.randint(0, len(list_not_max))
                
                ## ajout de certaines valeurs dans la liste des noeuds maximaux
                if nbr_not != 0 :
                    liste2=random.choices(list_not_max,weights=table_neigh_max,k=nbr_not)  
                    liste_node_max.extend(liste2)      
                
                for t in liste_node_max:
                    if not G.nodes[t]['visited']:
                        G.nodes[t]['visited'] = True
                        edge_index = G[n][t]['index']
                        edges.append(edge_index)
                        liste[t] = 1  
                                                            
                        if edge_index in honeypot1:
                                liste_edge.append(edge_index)
                                liste_node.extend([n,t])
                                nodes_out.append(n)
                                nodes_in.append(t)

                                for j in liste_node:
                                    liste_SR[j] = 1        
            
        
            
        edge_def1=edge_def(G,liste_node,liste_resist) 
        q.push_resist(liste,liste_resist,honeypot1)
        q.push_edges(edges,honeypot1)  
        q.push(liste)  
        q.push_defence(liste_SR,liste_edge,edge_def1,honeypot1)
        q.push_inv_edges(edges,honeypot1)

        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                             
            G.nodes[i]['visited'] = False
        
        node_IS = []
        for i in range(len(state)):
            if (state[i]==1):
                state[i]=(numpy.random.choice([0,1], p=[prob,(1-prob)]))
                if (state[i]== 0):
                    G.nodes[i]['visited'] = False
                    node_IS.append(i)
            if liste[i]==1:
                state[i] = state[i] + liste[i] 
      
        edge_IS = edge_def(G,node_IS,liste_resist)
        q.push_IS(node_IS,edge_IS,honeypot1)    

        q.new_attack(liste)
        q.step_state(state) 
        q.suscep_resist(honeypot1,liste_resist)

        honeypot1 = honey_pot(G,nodes_out,nodes_in,resist,liste_edge,liste_resist,nbr,nbr_smart)
        q.hospot_anime(honeypot1)          
            
           
def propagation_broadcast_smart(begin,G,q,resist,alpha,prob,nbr,nbr_smart):

    state = [0] * G.number_of_nodes() ### Tous les noeuds sont initialement susceptibles
    liste_neighbors = [list(G.neighbors(n)) for n in G.nodes] ### liste des listes de voisins

    # initialement, aucun sommet n'a été visité/traité
    nx.set_node_attributes(G, False, 'visited')
    
    state = begin_node(begin,state,G)
    q.push(state)
    
    liste_resist = resist_list(resist,state,G)
    honeypot1 = honey_pot(G,[],[],resist,[],liste_resist,nbr,0)
    
    q.push_resist(state,liste_resist,honeypot1)
    q.hospot_anime(honeypot1)
    q.step_state(state)
    
    
    while any(x in state for x in (0, 1)):
                
        liste = [0] * len(state)
        liste_SR = [0] * len(state)
        edges = []
        liste_edge =[]
        liste_node  =[]
        nodes_out = []
        nodes_in = []
        
        Suscep_Resist(G,state,liste,alpha,resist) 
        liste_resist = resist_list(resist,state,G) 
        
        
        for n in G.nodes:
            if (state[n] == 1):
                neighbors = liste_neighbors[G.nodes[n]['index']][:]
                list1=[]
                table_neigh =[]
                liste_node_max =[]
                ### voisins susceptibles
                for j in neighbors:
                    if (state[j] == 0):
                        list1.append(j)
                
                for i in list1:
                    list_smart= []
                    for j in (list(G.neighbors(i))):
                        if (state[j] == 0):
                            list_smart.append(j)
                    table_neigh.append(len(list_smart))
                if (len(table_neigh) > 0):
                    maxi = max(table_neigh) 
                else: 
                    maxi = 0
                
                for m in range(len(table_neigh)):
                    if table_neigh[m] == maxi:
                        liste_node_max.append(list1[m])

                for t in liste_node_max:
                    if not G.nodes[t]['visited']:
                        G.nodes[t]['visited'] = True
                        edge_index = G[n][t]['index']
                        edges.append(edge_index)
                        liste[t] = 1  
                                                            
                        if edge_index in honeypot1:
                            liste_edge.append(edge_index)
                            liste_node.extend([n,t])
                            nodes_out.append(n)
                            nodes_in.append(t)
                            for j in liste_node:
                                liste_SR[j] = 1             
            

        edge_def1=edge_def(G,liste_node,liste_resist) 

        q.push_resist(liste,liste_resist,honeypot1)
        q.push_edges(edges,honeypot1) 
        q.push(liste)
        q.push_defence(liste_SR,liste_edge,edge_def1,honeypot1)
        q.push_inv_edges(edges,honeypot1)        
        
        for i in liste_node:
            liste[i] = 0
            state[i] = 0                                                               
            G.nodes[i]['visited'] = False
         

        node_IS = []
    
        for i in range(len(state)):
            if (state[i]==1):
                state[i]=(numpy.random.choice([0,1], p=[prob,(1-prob)]))
                if (state[i]== 0):
                    G.nodes[i]['visited'] = False
                    node_IS.append(i)
            if liste[i]==1:
                state[i] = state[i] + liste[i] 


        edge_IS = edge_def(G,node_IS,liste_resist)
        q.push_IS(node_IS,edge_IS,honeypot1)

        q.new_attack(liste)
        q.step_state(state) 
        q.suscep_resist(honeypot1,liste_resist)

        honeypot1 = honey_pot(G,nodes_out,nodes_in,resist,liste_edge,liste_resist,nbr,nbr_smart)
        q.hospot_anime(honeypot1)          



### Retourne les aretes de liste_node qui ne sont pas résistantes
def edge_def(G, liste_node, liste_resist):
    edge_def =[]
    for i in liste_node:
        for j in list(G.neighbors(i)):
            index = G[i][j]['index']
            if ((index not in liste_resist) and (index not in edge_def)):
                edge_def.append(index)   
    return  edge_def


### Calcul des nouveaux noeuds résistants (S -> R)
def  Suscep_Resist(G, state, liste, alpha, resist):
    nv_resist = []
    for n in G.nodes:
        if (state[n] == 0):
            liste[n] = (numpy.random.choice([-1,0], p=[alpha,(1-alpha)]))
            if (liste[n] == -1):
                G.nodes[n]['visited'] = True 
                nv_resist.append(n)  
    resist.extend(nv_resist) 


### Noeuds infectés du départ
def begin_node(begin, state, G):
    for i in begin:  
        state[i] = 1
        G.nodes[i]['visited'] = True
    return state    


### Traitement des noeuds résistants de départ + retour des index des aretes liant un sommet résistant et un de ses voisins
def resist_list(resist, state, G):
    list_edge = []
    for j in resist:
        state[j] = -1
        G.nodes[j]['visited'] = True
        list_edge.extend((G[j][i]['index'] for i in G.neighbors(j)))
    return list_edge


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
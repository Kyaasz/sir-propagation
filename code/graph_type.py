###############################################################################################################
### Fichier contenant les différents types de graphe et les fonctions pour les générer (ancienne stagiaire) ###
###############################################################################################################

import networkx as nx
import math
import random
from scipy.spatial import Delaunay


def gen_in_disk(size):
    pts = []
    for i in range(size):
        t = 2*math.pi*random.random()
        u = random.random()+random.random()
        if u>1:
            r = 2-u 
        else:
            r = u
        pts.append((r*math.cos(t), r*math.sin(t)))
    
    return pts
        

def delaunay_graph(pts):
    G = nx.Graph()
    delaunay = Delaunay(pts)
    
    for s in delaunay.simplices:
    #    
    #for s in (n+1 for n in delaunay.simplices ):    
        for i in range(3):
            #print(s)
            v0 = s[i]
            v1 = s[(i+1)%3]
            #print('V0',v0,'V1',v1)
            G.add_edge(v0,v1)
   
    for i, n in enumerate(G.nodes):
        G.nodes[n]['index'] = i
    for i,e in enumerate(G.edges):
        G.edges[e]['index'] = i
    return G


# Generate Erdos-Renyi graph  
def erdos_reyni(size,P):
    G = nx.erdos_renyi_graph(size,P)
    for i, n in enumerate(G.nodes):
        G.nodes[n]['index'] = i
    for i,e in enumerate(G.edges):
        G.edges[e]['index'] = i
    return G


# Connected Erdos-Renyi graph
def gen_erdos_reyni(size,P) :
    G = erdos_reyni(size, P)
    while (not(nx.is_connected(G))):
        G = erdos_reyni(size, P)
    return G    
   
    
#Generate Small word network    
def small_word_network(size, m, P):
    G = nx.connected_watts_strogatz_graph(size, m, P,20)
     
    for i, n in enumerate(G.nodes):
            G.nodes[n]['index'] = i
    for i,e in enumerate(G.edges):
        G.edges[e]['index'] = i
    return G
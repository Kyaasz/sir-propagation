#### ANIMATION
from collections import Counter

class animator: 
    def __init__(self, G): 
        # attributs pour la couleur/largeur d'un noeud ou d'une arête
        self.node_suscep_color = "blue"
        self.node_infected_color = "salmon"
        self.node_contagious_color = "red"
        self.node_immune_color = "limegreen"
        self.edge_color = "black"
        self.edge_immune_color = "lightgray"
        self.edge_width = 1
        self.edge_immune_width = 0.5
        self.edge_attacked_width = 2
        self.edge_attacked_color = "red"
        self.edge_healing_color = "limegreen"
        # couleurs des noeuds et des arêtes du graphe
        self.nodes_colors = [self.node_suscep_color]*G.number_of_nodes()
        self.edges_colors = [self.edge_color]*G.number_of_edges()
        self.edges_widths = [self.edge_width]*G.number_of_edges()
        self.animation = {'node_colors':[], 
                          'edge_widths':[], 
                          'edge_colors':[]
                          }
        self.graph = G
        ## stats simulation
        self.nb_inf = []
        self.nb_imm = []
        self.nb_sus = []


    ## Ajouter une étape d'animation
    def append_animation(self): 
        self.animation['node_colors'].append(self.nodes_colors[:])
        self.animation['edge_widths'].append(self.edges_widths[:])
        self.animation['edge_colors'].append(self.edges_colors[:])


    ## Màj des noeuds_infectes
    def update_infected(self, infected):
        for i in infected: 
            self.nodes_colors[self.graph.nodes[i]['index']] = self.node_infected_color
        self.append_animation()

    def update_contagious(self, contagious): 
        for c in contagious: 
            self.nodes_colors[self.graph.nodes[c]['index']] = self.node_contagious_color
        self.append_animation() 


    ## Màj des arêtes attaquées
    def update_infected_edges(self, attacked): 
        for e in attacked: 
            self.edges_widths[e] = self.edge_attacked_width
            self.edges_colors[e] = self.edge_attacked_color
        self.append_animation()


    ## Retour à la normale des arêtes infectées
    def inv_update_infected_edges(self, attacked):
        for e in attacked: 
            self.edges_widths[e] = self.edge_width
            self.edges_colors[e] = self.edge_color
        self.append_animation()

    
    ## Màj des noeuds et des arêtes immunisés
    def update_immune(self, immune_nodes, immune_edges): 
        for n in immune_nodes:
            self.nodes_colors[self.graph.nodes[n]['index']] = self.node_immune_color
        for e in immune_edges:
            self.edges_colors[e] = self.edge_immune_color
            self.edges_widths[e] = self.edge_immune_width
        self.append_animation()

    
    ## Màj des arêtes par où passe l'antivirus
    def update_immune_edges(self, edges):
        for e in edges: 
            self.edges_colors[e] = self.edge_healing_color
            self.edges_widths[e] = self.edge_attacked_width
        self.append_animation()


    ## Màj des noeuds rétablis (i -> s)
    def update_recovered(self, recovered):
        for n in recovered:
            self.nodes_colors[self.graph.nodes[n]['index']] = self.node_suscep_color
        self.append_animation()

    
    ## Nombre d'infectés, susceptibles, immunisés par tour
    def state_step(self, state): 
        compte = Counter(state)
        self.nb_imm.append(compte[-1])
        self.nb_inf.append(compte[1])
        self.nb_sus.append(compte[0])

    
    ## Retourne les stats
    def stats(self): 
        return self.nb_inf, self.nb_sus, self.nb_imm
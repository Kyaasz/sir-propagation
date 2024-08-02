################################################
### Fichier pour l'animation des simulations ###
################################################

from collections import Counter

class animator: 
    def __init__(self, G): 
        # attributs pour la couleur/largeur d'un noeud ou d'une arête
        self.node_suscep_color = "lightgray"
        self.node_virus_a_color = "red"
        self.node_virus_b_color = "blue"
        self.edge_color = "black"
        self.edge_a_color = "red"
        self.edge_b_color = "blue"
        self.edge_width = 1
        self.edge_attacked_width = 2
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
        self.nb_a = []
        self.nb_b = []
        self.nb_sus = []


    ## Ajouter une étape d'animation
    def append_animation(self): 
        self.animation['node_colors'].append(self.nodes_colors[:])
        self.animation['edge_widths'].append(self.edges_widths[:])
        self.animation['edge_colors'].append(self.edges_colors[:])


    ## Màj des noeuds_infectes
    def update_infected_a_nodes(self, infected):
        for i in infected: 
            self.nodes_colors[self.graph.nodes[i]['index']] = self.node_virus_a_color
        self.append_animation()

    ## Màj des noeuds infectés
    def update_infected_b_nodes(self, infected):
        for i in infected: 
            self.nodes_colors[self.graph.nodes[i]['index']] = self.node_virus_b_color
        self.append_animation()


    ## Màj des arêtes attaquées
    def update_infected_a_edges(self, attacked): 
        for e in attacked: 
            self.edges_widths[e] = self.edge_attacked_width
            self.edges_colors[e] = self.edge_a_color
        self.append_animation()


    ## Màj des arêtes attaquées
    def update_infected_b_edges(self, attacked): 
        for e in attacked: 
            self.edges_widths[e] = self.edge_attacked_width
            self.edges_colors[e] = self.edge_b_color
        self.append_animation()


    ## Retour à la normale des arêtes infectées
    def inv_update_infected_edges(self, attacked):
        for e in attacked: 
            self.edges_widths[e] = self.edge_width
            self.edges_colors[e] = self.edge_color
        self.append_animation()
    

    ## Nombre d'infectés, susceptibles, immunisés par tour
    def state_step(self, state): 
        compte = Counter(state)
        self.nb_b.append(compte[-1])
        self.nb_a.append(compte[1])
        self.nb_sus.append(compte[0])

    
    ## Retourne les stats
    def stats(self): 
        return self.nb_a, self.nb_sus, self.nb_b
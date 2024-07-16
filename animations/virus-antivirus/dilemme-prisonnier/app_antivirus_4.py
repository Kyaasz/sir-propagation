###################################################################
############################ Imports ##############################
###################################################################
import time
from matplotlib.animation import writers
import graph_type
import networkx as nx
from IPython.display import HTML
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib import gridspec
plt.style.use('seaborn-v0_8')
from tkinter import * 
from tkinter.messagebox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import animated_graph
import virus_antivirus_propagation
import copy
from tkinter import filedialog
import os


#####################################################################
######################## Variables globales #########################
#####################################################################


spinboxes_inf = []
choicevideo = ""
G = nx.empty_graph(n=0, create_using=None)
nb_noeuds = 0 
nb_inf = 0
infectes = []
alpha = 0    ## probabilité de I vers S
infection_probability = 0     ## proba de propagation du virus
recovery_probability = 0 ## proba de propagation de l'antivirus
def_step = 0 ## etape à laquelle l'antivirus est injecté




#####################################################################
#####################################################################
#####################################################################
######################### Interface graphique #######################
#####################################################################
#####################################################################
#####################################################################


#####################################################################
############################# Fonctions #############################
#####################################################################

## fonction d'activation des boutons radios
def activation_radio(event = None):
    element = fenetre.focus_get()
    if isinstance(element, Radiobutton):
        element.invoke()

## fonction pour récupérer les valeurs d'une liste de spinboxes
def recup_liste_spin(liste_spinboxes): 
    return [int(s.get()) for s in liste_spinboxes]

## fonction pour vérifier qu'il n'y ait pas de doublon
def pas_de_doublon(l): 
    return (len(l) == len(set(l)))

## fonction d'affichage du message d'erreur
def show_message():
    showinfo("Il faut faire un choix")

## Fonction pour scroll
def scroll_fun(event):
    canv.configure(scrollregion=canv.bbox("all"))

def open_file():
    label_error12.pack_forget()
    global G
    file_path = filedialog.askopenfilename()
    if file_path: 
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1]
        if file_extension==".gexf":
            G = nx.read_gexf(file_name, node_type=int)
            debut_is()
        else:
            label_error12.pack()


#################


def choix_video(event=None):
    choix = value.get()
    if (choix not in ["1", "2"]):
        show_message()    
    else:
        ### valeur du choix de la vidéo
        global choicevideo
        choicevideo = choix
        ### reconstruction de la fenêtre
        frame1.pack_forget()
        frame2.pack(expand=True)
        bouton5.focus_set()


def choix_graphe(event=None):
    choix = value2.get()
    if (choix not in ["1", "2", "3"]):
        show_message()   
    elif (choix == "2"):  ### lecture du graphe
        global G
        G = nx.read_gexf("geeksforgeeks.gexf", node_type=int)
        frame2.pack_forget()
        debut_is() 
    elif (choix == "3"): 
        frame2.pack_forget()
        temp_button.pack()
    else:   ### construction d'un nouveau graphe 
        ### reconstruction de la fenêtre
        frame2.pack_forget()
        label3.pack()
        s.pack()
        bouton6.pack()
        s.focus_set()


def choix_nb_noeuds(event=None):
    choix = s.get()
    ### récupération du nombre de noeuds
    global nb_noeuds
    nb_noeuds = int(choix)

    ### reconstruction de la fenêtre
    label3.pack_forget()
    s.pack_forget()
    bouton6.pack_forget()
    label4.pack()
    bouton7.pack()
    bouton8.pack()
    bouton9.pack()
    bouton10.pack()
    bouton10.focus_set()


def choix_methode(event=None):
    global G
    choix = value3.get()
    match choix:
        case "1":
            label4.pack_forget()
            bouton7.pack_forget()
            bouton8.pack_forget()
            bouton9.pack_forget()
            bouton10.pack_forget()
            pts = graph_type.gen_in_disk(nb_noeuds)
            G = graph_type.delaunay_graph(pts)
            nx.write_gexf(G, "geeksforgeeks.gexf")
            debut_is()
        case "2":
            label4.pack_forget()
            bouton7.pack_forget()
            bouton8.pack_forget()
            bouton9.pack_forget()
            bouton10.pack_forget()
            label5.pack()
            entree1.pack()
            bouton11.pack()
            entree1.focus_set()
        case "3": 
            label4.pack_forget()
            bouton7.pack_forget()
            bouton8.pack_forget()
            bouton9.pack_forget()
            bouton10.pack_forget()
            label6.pack()
            entree2.pack()
            label7.pack()
            entree3.pack()
            bouton12.pack()
            entree2.focus_set()
        case _: 
            show_message()



def debut_is(event=None):
    ### récupération des valeurs
    global G
    choixp = value3.get()
    temp_button.pack_forget()
    label_error1.pack_forget()
    label_error2.pack_forget()
    label_error8.pack_forget()
    label_error9.pack_forget()
    match choixp: 

        case "2": ## on a construit un graphe avec la méthode de Erdos-Renyi
            p_graphe = value4.get()
            
            try: 
                proba_g_int = float(p_graphe)
                if ((proba_g_int> 1) or (proba_g_int<0)):
                    label_error2.pack()
                    entree1.focus_set()
                else : ## valeur correcte, on peut tenter de construire le graphe
                    G =  graph_type.erdos_reyni(nb_noeuds, proba_g_int)
                    if (not (nx.is_connected(G))):
                        label_error8.pack()
                        entree1.focus_set()
                    else:
                        nx.write_gexf(G, "geeksforgeeks.gexf") 
                        label5.pack_forget()
                        entree1.pack_forget()
                        bouton11.pack_forget()
                        label_error1.pack_forget()
                        label_error2.pack_forget()
                        labelis.pack()
                        entreeis.pack()
                        entreeis.focus_set()
                        boutonis.pack()
            except ValueError: 
                label_error1.pack()
                entree1.focus_set()

        case "3": ## on a construit un graphe avec la méthode Small-World
            p_graphe = value6.get()
            d_graphe = value5.get()
            
            try: 
                proba_g_int = float(p_graphe)
                d_graphe_int = int(d_graphe)
                if ((proba_g_int> 1) or (proba_g_int<0)):
                    label_error2.pack()
                    entree3.focus_set()
                elif (d_graphe_int >= nb_noeuds):
                    label_error9.pack()
                    entree2.focus_set()
                else : 
                    label6.pack_forget()
                    entree2.pack_forget()
                    label7.pack_forget()
                    entree3.pack_forget()
                    bouton12.pack_forget()
                    G = graph_type.small_word_network(nb_noeuds, d_graphe_int, proba_g_int)
                    nx.write_gexf(G, "geeksforgeeks.gexf")
                    labelis.pack()
                    entreeis.pack()
                    entreeis.focus_set()
                    boutonis.pack()
            except ValueError: 
                label_error1.pack() 
                entree2.focus_set()

        case _:
            ## création des nouveaux widgets
            labelis.pack()
            entreeis.pack()
            entreeis.focus_set()
            boutonis.pack()
            


def proba_is(event=None):
    label_error1.pack_forget()
    label_error2.pack_forget()
    global fig1
    global alpha 
    string_is = valueis.get()
    try: 
        p_is = float(string_is)
        if ((p_is > 1) or (p_is < 0)): 
            label_error2.pack()
            entreeis.focus_set()
        else:
            #### Affichage du graphe ###
            positions = nx.spring_layout(G)
            fig1, ax = plt.subplots()
            nx.draw(G, pos=positions, ax=ax, node_size=150, with_labels=True)
            ###############################

            # Création d'une fenêtre pour le graphe
            graph_window = Toplevel(fenetre)
            graph_window.title("Graphe")

            fenetre.update_idletasks() 
            x = fenetre.winfo_x()
            y = fenetre.winfo_y()
            width = fenetre.winfo_width()

            # Positionner la fenêtre du graphe à droite de la fenêtre principale
            graph_window.geometry(f"+{x + width + 10}+{y}")

            # Création d'un canvas pour afficher le graphe dans la fenêtre Tkinter
            canvas = FigureCanvasTkAgg(fig1, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack()
            alpha = p_is
            ## reconstruction de la fenêtre
            labelis.pack_forget()
            entreeis.pack_forget()
            boutonis.pack_forget()
            labelnbm.pack()
            snbm.pack()
            boutonnbm.pack()
            boutonnbm.focus_set()

    except ValueError:
        label_error1.pack()
        entreeis.focus_set()
    
    


def citer_malades(event=None):
    label_error3.pack_forget()
    global nb_inf
    choix = snbm.get()
    choix_int = int(choix)
    if (choix_int > G.number_of_nodes()):
        label_error3.pack()
        snbm.focus_set()
    else: 
        nb_inf = choix_int ## maj valeur
        ### affichage
        labelnbm.pack_forget()
        snbm.pack_forget()
        boutonnbm.pack_forget()
        if nb_inf > 0:
            ## création d'une nouvelle fenêtre pour les choix des noeuds
            frame_s_a.pack(expand=True)
            sc_v.pack(side='right', fill=Y)
            l = Label(frame_s_a, text="Entrer les indices des noeuds infectés")
            l.pack()
            canv.pack(expand=True)
            canv.create_window((0,0),window=framespinm, anchor=CENTER)
            framespinm.bind("<Configure>", scroll_fun)
            for i in range(int(choix)):
                temp_l = Label(framespinm, text="Indice du noeud infecté %s" % str(i+1))
                temp_l.pack()
                temp_spin = Spinbox(framespinm, from_=0, to=500) 
                spinboxes_inf.append(temp_spin)
                temp_spin.pack()
            boutoncm = Button(framespinm, text="Valider", command=recup_inf)
            boutoncm.bind("<Return>", recup_inf)
            boutoncm.pack()
            boutoncm.focus_set()
        else:
            recup_inf()



def recup_inf(event=None): 
    label_error3.pack_forget()
    label_error7.pack_forget()
    liste_valeurs = recup_liste_spin(spinboxes_inf)
    val_ok = all(v < G.number_of_nodes() for v in liste_valeurs)
    if val_ok and pas_de_doublon(liste_valeurs):
        infectes.extend(liste_valeurs)
        frame_s_a.destroy()
        labelds.pack()
        spinds.pack()
        boutonds.pack()
    elif val_ok:
        label_error7.pack()
    else : 
        label_error3.pack()


def choix_proba_inf(event=None):
    global def_step
    choix = spinds.get()
    choix_int = int(choix)
    def_step = choix_int
    ### affichage
    labelds.pack_forget()
    spinds.pack_forget()
    boutonds.pack_forget()
    labelinf.pack()
    entreeinf.pack()
    boutoninf.pack()
    entreeinf.focus_set()


def proba_anti(event=None):
    label_error1.pack_forget()
    label_error2.pack_forget()
    global infection_probability
    string_inf = valueinf.get()
    try: 
        p_inf = float(string_inf)
        if ((p_inf > 1) or (p_inf < 0)): 
            label_error2.pack()
            entreeinf.focus_set()
        else:
            infection_probability = p_inf
            ## reconstruction de la fenêtre
            labelinf.pack_forget()
            entreeinf.pack_forget()
            boutoninf.pack_forget()
            labelanti.pack()
            entreeanti.pack()
            entreeanti.focus_set()
            boutonanti.pack()
    except ValueError:
        label_error1.pack()
        entreeinf.focus_set()




def fin(event=None):
    plt.close(fig1)
    label_error1.pack_forget()
    label_error2.pack_forget()
    global recovery_probability
    label_error1.pack_forget()
    label_error2.pack_forget()
    string_anti = valueanti.get()
    try: 
        p_anti = float(string_anti)
        if ((p_anti > 1) or (p_anti < 0)): 
            label_error2.pack()
            entreeanti.focus_set()
        else:
            recovery_probability = p_anti
            ## reconstruction de la fenêtre
            fenetre.destroy()

    except ValueError:
        label_error1.pack()
        entreeinf.focus_set()




#####################################################################
############################# Composants ############################
#####################################################################


fenetre = Tk()
fenetre.geometry("500x500")

## Sélection de fichiers
temp_button = Button(fenetre, text="Sélectionner un fichier", command=open_file)
temp_button.bind("<Return>", open_file)

## choix vidéo
frame1 = Frame(fenetre)
label = Label(frame1, text="Enregistrer la vidéo de l'animation ? (Il faut avoir installé ffmpeg)")
label.pack()
value = StringVar()
bouton1 = Radiobutton(frame1, text="Oui", variable=value, value=1)
bouton2 = Radiobutton(frame1, text="Non", variable=value, value=2)
bouton1.bind("<Return>", activation_radio)
bouton2.bind("<Return>", activation_radio)
bouton1.pack(expand=True)
bouton2.pack(expand=True)
bouton = Button(frame1, text="Valider", command=choix_video)
bouton.bind("<Return>", choix_video)
bouton.pack()
frame1.pack(expand=True)
bouton.focus_set()



## choix du graphe
frame2 = Frame(fenetre)
label2 = Label(frame2, text="Construire un nouveau graphe, réutiliser le précédent ou importer un graphe ?")
label2.pack()
value2 = StringVar()
bouton3 = Radiobutton(frame2, text="Construire un nouveau graphe", variable=value2, value=1)
bouton3.bind("<Return>", activation_radio)
bouton3.pack()
bouton4 = Radiobutton(frame2, text="Reprendre l'ancien", variable=value2, value=2)
bouton4.bind("<Return>", activation_radio)
bouton4.pack()
bouton4b = Radiobutton(frame2, text="Importer un graphe (seuls les fichiers '.gexf' sont autorisés)", variable=value2, value=3)
bouton4b.bind("<Return>", activation_radio)
bouton4b.pack()
bouton5=Button(frame2, text="Valider", command=choix_graphe)
bouton5.pack()
bouton5.focus_set()
bouton5.bind("<Return>", choix_graphe)


## choix valeurs graphes
label3 = Label(fenetre, text="Choisir le nombre de noeuds du graphe")
s = Spinbox(fenetre, from_=1, to=500)
bouton6=Button(fenetre, text="Valider", command=choix_nb_noeuds)
bouton6.bind("<Return>", choix_nb_noeuds)


## choix de la méthode
label4 = Label(fenetre, text="Choix de la méthode de construction du graphe")
value3 = StringVar()
value3.set("")
bouton7 = Radiobutton(fenetre, text="Génération aléatoire", variable=value3, value=1)
bouton8 = Radiobutton(fenetre, text="Méthode d'Erdos-Renyi", variable=value3, value=2)
bouton9 = Radiobutton(fenetre, text="Graphe Small-World", variable=value3, value=3)
bouton7.bind("<Return>", activation_radio)
bouton8.bind("<Return>", activation_radio)
bouton9.bind("<Return>", activation_radio)
bouton10=Button(fenetre, text="Valider", command=choix_methode)
bouton10.bind("<Return>", choix_methode)


## config erdos-reyni
label5 = Label(fenetre, text="Entrer la probabilité d\'activation de chaque arête")
value4 = StringVar() 
value4.set("")
entree1 = Entry(fenetre, textvariable=value4, width=30)
bouton11=Button(fenetre, text="Valider", command=debut_is)
bouton11.bind("<Return>", debut_is)


## config small-world

label6 = Label(fenetre, text="Entrer le degré initial de chacun des sommets")
value5 = StringVar() 
value5.set("")
entree2 = Entry(fenetre, textvariable=value5, width=30)
label7 = Label(fenetre, text="Entrer la probabilité de modifier chacune des arêtes")
value6 = StringVar() 
value6.set("")
entree3 = Entry(fenetre, textvariable=value6, width=30)
bouton12=Button(fenetre, text="Valider", command=debut_is)
bouton12.bind("<Return>", debut_is)


## proba I -> S

labelis = Label(fenetre, text="Entrer la probabilité qu'un noeud passe de l'état I à S")
valueis = StringVar()
valueis.set("")
entreeis = Entry(fenetre, textvariable=valueis, width=30)
boutonis = Button(fenetre, text="Valider", command=proba_is)
boutonis.bind("<Return>", proba_is)

## nb noeuds malades

labelnbm = Label(fenetre, text="Entrer le nombre de noeuds infectés au début de la simulation")
snbm = Spinbox(fenetre, from_=0, to=500)
boutonnbm = Button(fenetre, text="Valider", command=citer_malades)
boutonnbm.bind("<Return>", citer_malades)

## lesquels

frame_s_a = Frame(fenetre)
canv = Canvas(frame_s_a)
framespinm = Frame(canv)
sc_v = Scrollbar(frame_s_a, orient='vertical', command = canv.yview)
canv.configure(yscrollcommand=sc_v.set)



## choix de l'étape de défense
labelds = Label(fenetre, text="Choisir l'étape à laquelle on introduit l'antivirus (il sera injecté dans un noeud tiré aléatoirement)")
spinds = Spinbox(fenetre, from_=0, to=500)
boutonds = Button(fenetre, text="Valider", command=choix_proba_inf)
boutonds.bind("<Return>", choix_proba_inf)


### choix de la proba d'infection
labelinf = Label(fenetre, text="Entrer la probabilité qu'un noeud infecté propage le virus")
valueinf = StringVar()
valueinf.set("")
entreeinf = Entry(fenetre, textvariable=valueinf, width=30)
boutoninf = Button(fenetre, text="Valider", command=proba_anti)
boutoninf.bind("<Return>", proba_anti)

### choix proba recovery
labelanti = Label(fenetre, text="Entrer la probabilité qu'un noeud propage l'antivirus")
valueanti = StringVar()
valueanti.set("")
entreeanti = Entry(fenetre, textvariable=valueanti, width=30)
boutonanti = Button(fenetre, text="Lancer la simulation", command=fin)
boutonanti.bind("<Return>", fin)



## label d'erreur
label_error2 = Label(fenetre, text = "Veuillez entrer une valeur entre 0 et 1")
label_error1 = Label(fenetre, text = "Veuillez entrer une valeur numérique")
label_error3 = Label(fenetre, text = "Veuillez renseigner une valeur inférieure au nombre total de noeuds")
label_error7 = Label(fenetre, text = "La liste suggérée contient des doublons")
label_error8 = Label(fenetre, text = "Augmenter la probabilité d'activation, le graphe n'est pas connexe") 
label_error9 = Label(fenetre, text = "Le degré choisi ne peut pas excéder la taille du graphe")
label_error10 = Label(fenetre, text = "Le nombre de noeuds résistants choisi ne peut pas respecter la taille du graphe")
label_error12 = Label(fenetre, text = "Le fichier sélectionné ne respecte pas le format 'gexf'")

fenetre.mainloop()





###################################################################
################### Lancement de la simulation ####################
###################################################################
G_init = copy.deepcopy(G)
G1 = copy.deepcopy(G_init)
G2 = copy.deepcopy(G_init)
G3 = copy.deepcopy(G_init)
G4 = copy.deepcopy(G_init)
q_uu = animated_graph.animator(G1) 
q_ub = animated_graph.animator(G2)   
q_bu = animated_graph.animator(G3)  
q_bb = animated_graph.animator(G4)      

t_debut = time.time()

virus_antivirus_propagation.unicast_competing_propagation(G1, infectes, alpha, def_step, infection_probability, recovery_probability, q_uu)
virus_antivirus_propagation.broadcast_competing_propagation(G4, infectes, alpha, def_step, infection_probability, recovery_probability, q_bb)
virus_antivirus_propagation.unicast_virus_competing_propagation(G2, infectes, alpha, def_step, infection_probability, recovery_probability, q_ub)
virus_antivirus_propagation.unicast_antivirus_competing_propagation(G3, infectes, alpha, def_step, infection_probability, recovery_probability, q_bu)

t_fin = time.time()

print("TEMPS = ", t_fin - t_debut)


### Affichage / Animation
   
positions = nx.spring_layout(G)  # positions for all nodes
fig = plt.figure(figsize=(14, 14))
gs = gridspec.GridSpec(2, 2)
axbb = fig.add_subplot(gs[1,1])
axuu = fig.add_subplot(gs[0,0])
axub = fig.add_subplot(gs[0,1])
axbu = fig.add_subplot(gs[1,0])
axuu.clear()
axbb.clear()
axub.clear()
axbu.clear()
line1 = plt.scatter([], [], c="salmon", marker='o')
line2 = plt.scatter([], [], c="limegreen", marker='o')
line3 = plt.scatter([], [], c="blue", marker='o')

########################

def updateuu(frame):
    axuu.clear()
    axuu.set_title("Unicast virus, unicast antivirus", fontweight = 'bold')
    axuu.legend((line3, line1, line2), ('susceptible', 'infected', 'immune'), numpoints=1, loc='best')
    nx.draw(
        G1,
        pos=positions,
        ax=axuu,
        node_size=250,
        with_labels=True,
        font_size=10,
        node_color=q_uu.animation['node_colors'][frame],
        edge_color=q_uu.animation['edge_colors'][frame],
        width=q_uu.animation['edge_widths'][frame])


ani_uu = matplotlib.animation.FuncAnimation(fig,
                                         updateuu,
                                         frames=len(q_uu.animation['edge_colors']),
                                         interval=500,
                                         repeat=False)

########################

def updatebb(frame):
    axbb.clear()
    axbb.set_title("Broadcast virus, broadcast antivirus", fontweight = 'bold')
    axbb.legend((line3, line1, line2), ('susceptible', 'infected', 'immune'), numpoints=1, loc='best')
    nx.draw(  
        G4,
        pos=positions,
        ax=axbb,
        node_size=250,
        with_labels=True,
        font_size=10,
        node_color=q_bb.animation['node_colors'][frame],
        edge_color=q_bb.animation['edge_colors'][frame],
        width=q_bb.animation['edge_widths'][frame])


ani_bb = matplotlib.animation.FuncAnimation(fig,
                                         updatebb,
                                         frames=len(q_bb.animation['edge_colors']),
                                         interval=500,
                                         repeat=False)

########################

def updateub(frame):
    axub.clear()
    axub.set_title("Unicast virus, broadcast antivirus", fontweight="bold")
    axub.legend((line3, line1, line2), ('susceptible', 'infected', 'immune'), numpoints=1, loc='best')
    nx.draw(
        G2,
        pos=positions,
        ax=axub,
        node_size=250,
        with_labels=True,
        font_size=10,
        node_color=q_ub.animation['node_colors'][frame],
        edge_color=q_ub.animation['edge_colors'][frame],
        width=q_ub.animation['edge_widths'][frame])


ani_ub = matplotlib.animation.FuncAnimation(fig,
                                         updateub,
                                         frames=len(q_ub.animation['edge_colors']),
                                         interval=500,
                                         repeat=False)
########################

def updatebu(frame):
    axbu.clear()
    axbu.set_title("Broadcast virus, unicast antivirus", fontweight = 'bold')
    axbu.legend((line3, line1, line2), ('susceptible', 'infected', 'immune'), numpoints=1, loc='best')
    nx.draw(
        G3,
        pos=positions,
        ax=axbu,
        node_size=250,
        with_labels=True,
        font_size=10,
        node_color=q_bu.animation['node_colors'][frame],
        edge_color=q_bu.animation['edge_colors'][frame],
        width=q_bu.animation['edge_widths'][frame])


ani_bu = matplotlib.animation.FuncAnimation(fig,
                                         updatebu,
                                         frames=len(q_bu.animation['edge_colors']),
                                         interval=500,
                                         repeat=False)

bb = axbb.get_position()
bu = axbu.get_position()
ub = axub.get_position()
uu = axuu.get_position()

# Draw horizontal line
line = plt.Line2D([0, 1], [0.5, 0.5], color="black", linewidth=1.5, transform=fig.transFigure, figure=fig)
fig.lines.append(line)

# Draw vertical line
line = plt.Line2D([0.5, 0.5], [0, 1], color="black", linewidth=1.5, transform=fig.transFigure, figure=fig)
fig.lines.append(line)


if choicevideo ==  "1" : #Uniquement si ffmpeg est installé
    Writer = writers['ffmpeg']
    writer = Writer(
        fps=2,
        metadata=dict(artist="oumaima diami", title = "AnimationPlt"),
        bitrate=8000)

    ani_bb.save("AnimationPlt_bb.mp4", writer=writer)
    HTML(ani_bb.to_html5_video())
    ani_uu.save("AnimationPlt_uu.mp4", writer=writer)
    HTML(ani_uu.to_html5_video())
    ani_ub.save("AnimationPlt_ub.mp4", writer=writer)
    HTML(ani_ub.to_html5_video())
    ani_bu.save("AnimationPlt_bu.mp4", writer=writer)
    HTML(ani_bu.to_html5_video())

    plt.show()
else :

    plt.show()
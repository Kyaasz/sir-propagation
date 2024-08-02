##################################################################
### Fichier de lancement de l'application - virus et antivirus ###
##################################################################


############################ Imports ##############################

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
from tkinter import filedialog
import os

######################## Variables globales #########################

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
propa = ""


#####################################################################
######################### Interface graphique #######################
#####################################################################


############################# Fonctions #############################

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


#####################################
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
        G = nx.read_gexf("graph.gexf", node_type=int)
        frame2.pack_forget()
        debut_is() 
    elif (choix == "3"): 
        frame2.pack_forget()
        temp_button.pack()
    else:   ### construction d'un nouveau graphe 
        ### reconstruction de la fenêtre
        frame2.pack_forget()
        frame_nb_n.pack(expand=True)
        s.focus_set()


def choix_nb_noeuds(event=None):
    choix = s.get()
    ### récupération du nombre de noeuds
    global nb_noeuds
    nb_noeuds = int(choix)

    ### reconstruction de la fenêtre
    frame_nb_n.pack_forget()
    frame_met_g.pack(expand=True)
    bouton10.focus_set()


def choix_methode(event=None):
    global G
    choix = value3.get()
    match choix:
        case "1":
            frame_met_g.pack_forget()
            pts = graph_type.gen_in_disk(nb_noeuds)
            G = graph_type.delaunay_graph(pts)
            nx.write_gexf(G, "graph.gexf")
            debut_is()
        case "2":
            frame_met_g.pack_forget()
            frame_er.pack(expand=True)
            entree1.focus_set()
        case "3": 
            frame_met_g.pack_forget()
            frame_sw.pack(expand=True)
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
                        nx.write_gexf(G, "graph.gexf") 
                        frame_er.pack_forget()
                        label_error1.pack_forget()
                        label_error2.pack_forget()
                        frame_is.pack(expand=True)
                        entreeis.focus_set()
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
                    frame_sw.pack_forget()
                    G = graph_type.small_word_network(nb_noeuds, d_graphe_int, proba_g_int)
                    nx.write_gexf(G, "graph.gexf")
                    frame_is.pack(expand=True)
                    entreeis.focus_set()
            except ValueError: 
                label_error1.pack() 
                entree2.focus_set()

        case _:
            ## création des nouveaux widgets
            frame_is.pack(expand=True)
            entreeis.focus_set()
            


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
            frame_is.pack_forget()
            frame_nbm.pack(expand=True)
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
        frame_nbm.pack_forget()
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
        frame_ds.pack(expand=True)
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
    frame_ds.pack_forget()
    frame_inf.pack(expand=True)
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
            frame_inf.pack_forget()
            frame_anti.pack(expand=True)
            entreeanti.focus_set()
    except ValueError:
        label_error1.pack()
        entreeinf.focus_set()




def choix_propa(event=None):
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
            frame_anti.pack_forget()
            framepropa.pack(expand=True)
            boutonvp.focus_set()

    except ValueError:
        label_error1.pack()
        entreeinf.focus_set()


def fin(event=None):
    global propa
    choix = valpropa.get()
    if (choix not in ["1", "2", "3", "4", "5"]):
        show_message()   
    else : 
        propa = choix
        fenetre.destroy()


############################# Composants ############################

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
bouton3 = Radiobutton(frame2, text="Construire un nouveau graphe (Cela écrasera 'graph.gexf')", variable=value2, value=1)
bouton3.bind("<Return>", activation_radio)
bouton3.pack()
bouton4 = Radiobutton(frame2, text="Reprendre l'ancien ('graph.gexf')", variable=value2, value=2)
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
frame_nb_n = Frame(fenetre)
label3 = Label(frame_nb_n, text="Choisir le nombre de noeuds du graphe")
s = Spinbox(frame_nb_n, from_=1, to=500)
bouton6=Button(frame_nb_n, text="Valider", command=choix_nb_noeuds)
bouton6.bind("<Return>", choix_nb_noeuds)
label3.pack()
s.pack()
bouton6.pack()


## choix de la méthode
frame_met_g = Frame(fenetre)
label4 = Label(frame_met_g, text="Choix de la méthode de construction du graphe")
value3 = StringVar()
value3.set("")
bouton7 = Radiobutton(frame_met_g, text="Génération aléatoire", variable=value3, value=1)
bouton8 = Radiobutton(frame_met_g, text="Méthode d'Erdos-Renyi", variable=value3, value=2)
bouton9 = Radiobutton(frame_met_g, text="Graphe Small-World", variable=value3, value=3)
bouton7.bind("<Return>", activation_radio)
bouton8.bind("<Return>", activation_radio)
bouton9.bind("<Return>", activation_radio)
bouton10=Button(frame_met_g, text="Valider", command=choix_methode)
bouton10.bind("<Return>", choix_methode)
label4.pack()
bouton7.pack()
bouton8.pack()
bouton9.pack()
bouton10.pack()


## config erdos-reyni
frame_er = Frame(fenetre)
label5 = Label(frame_er, text="Entrer la probabilité d\'activation de chaque arête")
value4 = StringVar() 
value4.set("")
entree1 = Entry(frame_er, textvariable=value4, width=30)
bouton11=Button(frame_er, text="Valider", command=debut_is)
bouton11.bind("<Return>", debut_is)
label5.pack()
entree1.pack()
bouton11.pack()

## config small-world

frame_sw = Frame(fenetre)
label6 = Label(frame_sw, text="Entrer le degré initial de chacun des sommets")
value5 = StringVar() 
value5.set("")
entree2 = Entry(frame_sw, textvariable=value5, width=30)
label7 = Label(frame_sw, text="Entrer la probabilité de modifier chacune des arêtes")
value6 = StringVar() 
value6.set("")
entree3 = Entry(frame_sw, textvariable=value6, width=30)
bouton12=Button(frame_sw, text="Valider", command=debut_is)
bouton12.bind("<Return>", debut_is)
label6.pack()
entree2.pack()
label7.pack()
entree3.pack()
bouton12.pack()


## proba I -> S

frame_is = Frame(fenetre)
labelis = Label(frame_is, text="Entrer la probabilité qu'un noeud passe de l'état I à S")
valueis = StringVar()
valueis.set("")
entreeis = Entry(frame_is, textvariable=valueis, width=30)
boutonis = Button(frame_is, text="Valider", command=proba_is)
boutonis.bind("<Return>", proba_is)
labelis.pack()
entreeis.pack()
boutonis.pack()
## nb noeuds malades

frame_nbm = Frame(fenetre)
labelnbm = Label(frame_nbm, text="Entrer le nombre de noeuds infectés au début de la simulation")
snbm = Spinbox(frame_nbm, from_=0, to=500)
boutonnbm = Button(frame_nbm, text="Valider", command=citer_malades)
boutonnbm.bind("<Return>", citer_malades)
labelnbm.pack()
snbm.pack()
boutonnbm.pack()

## lesquels
frame_s_a = Frame(fenetre)
canv = Canvas(frame_s_a)
framespinm = Frame(canv)
sc_v = Scrollbar(frame_s_a, orient='vertical', command = canv.yview)
canv.configure(yscrollcommand=sc_v.set)



## choix de l'étape de défense
frame_ds = Frame(fenetre)
labelds = Label(frame_ds, text="Choisir l'étape à laquelle on introduit l'antivirus (il sera injecté dans un noeud tiré aléatoirement)")
spinds = Spinbox(frame_ds, from_=0, to=500)
boutonds = Button(frame_ds, text="Valider", command=choix_proba_inf)
boutonds.bind("<Return>", choix_proba_inf)
labelds.pack()
spinds.pack()
boutonds.pack()


### choix de la proba d'infection
frame_inf = Frame(fenetre)
labelinf = Label(frame_inf, text="Entrer la probabilité qu'un noeud infecté propage le virus")
valueinf = StringVar()
valueinf.set("")
entreeinf = Entry(frame_inf, textvariable=valueinf, width=30)
boutoninf = Button(frame_inf, text="Valider", command=proba_anti)
boutoninf.bind("<Return>", proba_anti)
labelinf.pack()
entreeinf.pack()
boutoninf.pack()

### choix proba recovery
frame_anti = Frame(fenetre)
labelanti = Label(frame_anti, text="Entrer la probabilité qu'un noeud propage l'antivirus")
valueanti = StringVar()
valueanti.set("")
entreeanti = Entry(frame_anti, textvariable=valueanti, width=30)
boutonanti = Button(frame_anti, text="Valider", command=choix_propa)
boutonanti.bind("<Return>", choix_propa)
labelanti.pack()
entreeanti.pack()
boutonanti.pack()



## choix de la propagation
framepropa = Frame(fenetre)
labelpropa = Label(framepropa, text="Quel type de propagation utiliser ?")
labelpropa.pack()
valpropa = StringVar()
bouton1_propa = Radiobutton(framepropa, text="Propagation unicast, propagation un à un", variable=valpropa, value=1)
bouton1_propa.bind("<Return>", activation_radio)
bouton1_propa.pack()
bouton2_propa = Radiobutton(framepropa, text="Propagation broadcast, diffusion à tous les voisins", variable=valpropa, value=2)
bouton2_propa.bind("<Return>", activation_radio)
bouton2_propa.pack()
bouton3_propa = Radiobutton(framepropa, text="Propagation unicast avec délai avant l'état contagieux", variable=valpropa, value=3)
bouton3_propa.bind("<Return>", activation_radio)
bouton3_propa.pack()
bouton4_propa = Radiobutton(framepropa, text="Propagation unicast pour le virus, broadcast pour l'antivirus", variable=valpropa, value=4)
bouton4_propa.bind("<Return>", activation_radio)
bouton4_propa.pack()
bouton5_propa = Radiobutton(framepropa, text="Propagation broadcast pour le virus, unicast pour l'antivirus", variable=valpropa, value=5)
bouton5_propa.bind("<Return>", activation_radio)
bouton5_propa.pack()
boutonvp=Button(framepropa, text="Valider", command=fin)
boutonvp.pack()
boutonvp.focus_set()
boutonvp.bind("<Return>", fin)



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



################### Lancement de la simulation ####################

q = animated_graph.animator(G)    

t_debut = time.time()

match propa:
    case "1":
        virus_antivirus_propagation.unicast_competing_propagation(G, infectes, alpha, def_step, infection_probability, recovery_probability, q)
    case "2": 
        virus_antivirus_propagation.broadcast_competing_propagation(G, infectes, alpha, def_step, infection_probability, recovery_probability, q)
    case "3":
        virus_antivirus_propagation.unicast_competing_contagious_propagation(G, infectes, alpha, def_step, infection_probability, recovery_probability, q)
    case "4":
        virus_antivirus_propagation.unicast_virus_competing_propagation(G, infectes, alpha, def_step, infection_probability, recovery_probability, q)
    case "5":
        virus_antivirus_propagation.unicast_antivirus_competing_propagation(G, infectes, alpha, def_step, infection_probability, recovery_probability, q)    
    case _:
        pass

t_fin = time.time()

print("TEMPS = ", t_fin - t_debut)


### Affichage / Animation
   
positions = nx.spring_layout(G)  # positions for all nodes
fig = plt.figure(figsize=(10, 10))
gs = gridspec.GridSpec(2, 2, height_ratios=[3,2])
ax = fig.add_subplot(gs[:-1, :])
ax.clear()
s1 = plt.scatter([], [], c="salmon", marker='o')
s2 = plt.scatter([], [], c="limegreen", marker='o')
s3 = plt.scatter([], [], c="blue", marker='o')
s4 = plt.scatter([], [], c="red", marker='o')

compt = 0



def update(frame):
    global propa
    ax.clear()
    ax.set_title("Competing virus and antivirus", fontweight='bold', fontsize=10, y=0)
    if propa !="3":
        ax.legend((s3, s1, s2), ('susceptible', 'infected', 'immune'), loc='best')
    else:
        ax.legend((s3, s1, s4, s2), ('susceptible', 'infected', 'contagious', 'immune'), loc='best')
    nx.draw(
        G,
        pos=positions,
        ax=ax,
        node_size=250,
        with_labels=True,
        font_size=10,
        node_color=q.animation['node_colors'][frame],
        edge_color=q.animation['edge_colors'][frame],
        width=q.animation['edge_widths'][frame])


ani = matplotlib.animation.FuncAnimation(fig,
                                         update,
                                         frames=len(q.animation['edge_colors']),
                                         interval=500,
                                         repeat=False)


# Draw horizontal line
line = plt.Line2D([0, 1], [0.45, 0.45], color="black", linewidth=1, transform=fig.transFigure, figure=fig)
fig.lines.append(line)

## PLOT THE GRAPH
ax2 = fig.add_subplot(gs[-1, :])
l1,l2,l3 = q.stats()
x1 = []
plt.grid( which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid( which='minor', color='#999999', linestyle='-', alpha=0.2)
for n in  range(len(l1)) :
	x1.append(n)
ax2.set(xlim=[-1,len(x1)+1], ylim=[-1, G.number_of_nodes()+1], xlabel='Time [step]', ylabel='Population [Individual]')
ax2.set_title("Evolution of the populations across time", fontweight='bold', fontsize=10)
line2 = ax2.plot(x1[0], l2[0], color='blue',label='susceptible')[0]
line1 = ax2.plot(x1[0], l1[0], color='red',label='infected')[0]
line3 = ax2.plot(x1[0], l3[0], color='limegreen',label='immune')[0]
plt.legend()
plt.tight_layout()
def update_funcs(frame): 
    line1.set_xdata(x1[:frame])
    line2.set_xdata(x1[:frame])
    line3.set_xdata(x1[:frame])
    line1.set_ydata(l1[:frame])
    line2.set_ydata(l2[:frame])
    line3.set_ydata(l3[:frame])
    return(line1, line2, line3)

ani2 = matplotlib.animation.FuncAnimation(fig,
                                          update_funcs,
                                          frames = len(x1)+1,
                                          interval = 50,
                                          repeat = False)


if choicevideo ==  "1" : #Uniquement si ffmpeg est installé
    Writer = writers['ffmpeg']
    writer = Writer(
        fps=2,
        metadata=dict(artist="y", title = "AnimationPlt"),
        bitrate=8000)

    ani.save("AnimationPlt.mp4", writer=writer)
    HTML(ani.to_html5_video())

    plt.show()
else :

    plt.show()
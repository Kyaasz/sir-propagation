###########################################################################################
### Fichier qui lance l'application graphique de simulations pour les virus concurrents ###
###########################################################################################


############################ Imports ##############################

import time
from matplotlib.animation import writers
import competing_propag
import animated_graph
import graph_type
import networkx as nx
from IPython.display import HTML
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib import gridspec
plt.style.use('seaborn-v0_8')
from tkinter import * 
from tkinter.messagebox import *
from tkinter import filedialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



######################## Variables globales #########################



spinboxes_infa = []
spinboxes_infb = []
choicevideo = ""
G = nx.empty_graph(n=0, create_using=None)
nb_noeuds = 0 
nb_inf_a = 0 
nb_inf_b = 0 
infectes_a = []
infectes_b = []
p_inf_a = 0
p_inf_b = 0

#####################################################################
######################### Interface graphique #######################
#####################################################################


############################# Fonctions #############################

def activation_radio(event = None):
    element = fenetre.focus_get()
    if isinstance(element, Radiobutton):
        element.invoke()


def recup_liste_spin(liste_spinboxes): 
    return [int(s.get()) for s in liste_spinboxes]

def pas_de_doublon(l): 
    return (len(l) == len(set(l)))

def show_message():
    showinfo("Il faut faire un choix")

def scroll_fun(event):
    canv.configure(scrollregion=canv.bbox("all"))

def scroll_fun2(event):
    canvb.configure(scrollregion=canvb.bbox("all"))

def open_file():
    label_error12.pack_forget()
    global G
    file_path = filedialog.askopenfilename()
    if file_path: 
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1]
        if file_extension==".gexf":
            G = nx.read_gexf(file_name, node_type=int)
            debut_nb_a()
        else:
            label_error12.pack()



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
    label_error12.pack_forget()
    global G
    choix = value2.get()
    if (choix not in ["1", "2", "3"]):
        show_message()   
    elif (choix == "2"):  ### lecture du graphe
        G = nx.read_gexf("graph.gexf", node_type=int)
        frame2.pack_forget()
        debut_nb_a() 
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
            debut_nb_a()
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



def debut_nb_a(event=None):
    ### récupération des valeurs
    global G
    temp_button.pack_forget()
    choixp = value3.get()
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
                        frame_nb_a.pack(expand=True)
                        bouton_nb_a.focus_set()
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
                    frame_nb_a.pack(expand=True)
                    bouton_nb_a.focus_set()
            except ValueError: 
                label_error1.pack() 
                entree2.focus_set()

        case _:
            ## création des nouveaux widgets
            frame_nb_a.pack(expand=True)
            bouton_nb_a.focus_set()
            




def choix_inf_a(event=None):


    global nb_inf_a
    choix = spin_nb_a.get()
    choix_int = int(choix)
    if (choix_int > G.number_of_nodes()):
        label_error3.pack()
        spin_nb_a.focus_set()
    else:
        #### Affichage du graphe ###
        global fig1
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

        
        nb_inf_a = choix_int
        label_error3.pack_forget()
        frame_nb_a.pack_forget()
        if nb_inf_a > 0:
            ## création d'une nouvelle fenêtre pour les choix des noeuds
            frame_s_a.pack(expand=True)
            sc_v.pack(side='right', fill=Y)
            l = Label(frame_s_a, text="Entrer les indices des noeuds infectés par A")
            l.pack()
            canv.pack(expand=True)
            canv.create_window((0,0),window=framespina, anchor=CENTER)
            framespina.bind("<Configure>", scroll_fun)
            for i in range(int(choix)):
                temp_l = Label(framespina, text="Indice du noeud infecté %s" % str(i+1))
                temp_l.pack()
                temp_spin = Spinbox(framespina, from_=0, to=500) 
                spinboxes_infa.append(temp_spin)
                temp_spin.pack()
            boutoncm = Button(framespina, text="Valider", command=recup_infa)
            boutoncm.bind("<Return>", recup_infa)
            boutoncm.pack()
            boutoncm.focus_set()
        else:
            recup_infa()



def recup_infa(event=None): 
    label_error3.pack_forget()
    label_error7.pack_forget()
    liste_valeurs = recup_liste_spin(spinboxes_infa)
    val_ok = all(v < G.number_of_nodes() for v in liste_valeurs)
    if val_ok and pas_de_doublon(liste_valeurs):
        infectes_a.extend(liste_valeurs)
        frame_s_a.destroy()
        frame_nb_b.pack(expand=True)
        bouton_nb_b.focus_set()
    elif val_ok:
        label_error7.pack()
    else : 
        label_error3.pack()


def choix_inf_b(event=None):
    global nb_inf_b
    choix = spin_nb_b.get()
    choix_int = int(choix)
    if (choix_int > G.number_of_nodes() - nb_inf_a):
        label_error10.pack()
    else: 
        nb_inf_b = choix_int
        ###
        frame_nb_b.pack_forget()
        if nb_inf_b >0:
            frame_s_b.pack(expand=True)
            sc_v2.pack(side='right', fill=Y)
            l = Label(frame_s_b, text="Entrer les indices des noeuds infectés par B")
            l.pack()
            canvb.pack(expand=True)
            canvb.create_window((0,0),window=framespinb, anchor=CENTER)
            framespinb.bind("<Configure>", scroll_fun2)
            for i in range(int(choix)):
                temp_l = Label(framespinb, text="Indice du noeud infecté %s" % str(i+1))
                temp_l.pack()
                temp_spin = Spinbox(framespinb, from_=0, to=500)
                spinboxes_infb.append(temp_spin)
                temp_spin.pack()
            boutoncm = Button(framespinb, text="Valider", command=prob_a)
            boutoncm.bind("<Return>", prob_a)
            boutoncm.pack()
            boutoncm.focus_set()
        else:
            prob_a()


def prob_a(event=None): 
    label_error3.pack_forget()
    label_error4.pack_forget()
    label_error7.pack_forget()
    label_error10.pack_forget()
    liste_valeurs = recup_liste_spin(spinboxes_infb)
    val_ok = all(v < G.number_of_nodes() for v in liste_valeurs)
    non_inf = all((v not in infectes_a) for v in liste_valeurs)
    if val_ok and non_inf and pas_de_doublon(liste_valeurs):
        infectes_b.extend(liste_valeurs)
        frame_s_b.destroy()
        plt.close(fig1)
        frame_pa.pack(expand=True)
        entreepa.focus_set()
    elif val_ok and non_inf:
        label_error7.pack()
    elif val_ok:
        label_error4.pack()
    else:
        label_error3.pack()


def prob_b(event=None):
    label_error1.pack_forget()
    label_error2.pack_forget() 
    global p_inf_a
    p_a = valuepa.get()
    try: 
        p_a_int = float(p_a)
        if ((p_a_int> 1) or (p_a_int<0)):
            label_error2.pack()
            entreepa.focus_set()
        else : 
            p_inf_a = p_a_int
            frame_pa.pack_forget()
            frame_pb.pack(expand=True)
            entreepb.focus_set()
    except ValueError: 
        label_error1.pack()
        entreepa.focus_set()
        


def fin(event=None): 
    label_error1.pack_forget()
    label_error2.pack_forget()
    global p_inf_b
    p_b = valuepb.get()
    try: 
        p_b_int = float(p_b)
        if ((p_b_int> 1) or (p_b_int<0)):
            label_error2.pack()
            entreepb.focus_set()
        else : 
            p_inf_b = p_b_int
            frame_pb.pack_forget()
            fenetre.destroy()
    except ValueError: 
        label_error1.pack()
        entreepb.focus_set()


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
bouton11=Button(frame_er, text="Valider", command=debut_nb_a)
bouton11.bind("<Return>", debut_nb_a)
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
bouton12=Button(frame_sw, text="Valider", command=debut_nb_a)
bouton12.bind("<Return>", debut_nb_a)
label6.pack()
entree2.pack()
label7.pack()
entree3.pack()
bouton12.pack()

## nb noeuds inf par a
frame_nb_a = Frame(fenetre)
label_nb_a = Label(frame_nb_a, text="Choisir le nombre de noeuds infectés par A au départ")
spin_nb_a = Spinbox(frame_nb_a, from_=0,to=500)
bouton_nb_a = Button(frame_nb_a, text= "Valider", command=choix_inf_a)
bouton_nb_a.bind("<Return>", choix_inf_a)
label_nb_a.pack()
spin_nb_a.pack()
bouton_nb_a.pack()

## lesquels
frame_s_a = Frame(fenetre)
canv = Canvas(frame_s_a)
framespina = Frame(canv)
sc_v = Scrollbar(frame_s_a, orient='vertical', command = canv.yview)
canv.configure(yscrollcommand=sc_v.set)

## nb noeuds inf par n
frame_nb_b = Frame(fenetre)
label_nb_b = Label(frame_nb_b, text="Choisir le nombre de noeuds infectés par B au départ")
spin_nb_b = Spinbox(frame_nb_b, from_=0,to=500)
bouton_nb_b = Button(frame_nb_b, text= "Valider", command=choix_inf_b)
bouton_nb_b.bind("<Return>", choix_inf_b)
label_nb_b.pack()
spin_nb_b.pack()
bouton_nb_b.pack()


## lesquels
frame_s_b = Frame(fenetre)
canvb = Canvas(frame_s_b)
framespinb = Frame(canvb)
sc_v2 = Scrollbar(frame_s_b, orient='vertical', command = canvb.yview)
canvb.configure(yscrollcommand=sc_v2.set)

## proba infection A
frame_pa = Frame(fenetre)
labelpa = Label(frame_pa, text="Entrer la probabilité qu'un noeud partage le virus A")
valuepa = StringVar()
valuepa.set("")
entreepa = Entry(frame_pa, textvariable=valuepa, width=30)
boutonpa = Button(frame_pa, text="Valider", command=prob_b)
boutonpa.bind("<Return>", prob_b)
labelpa.pack()
entreepa.pack()
boutonpa.pack()


## proba infection B
frame_pb = Frame(fenetre)
labelpb = Label(frame_pb, text="Entrer la probabilité qu'un noeud partage le virus B")
valuepb = StringVar()
valuepb.set("") 
entreepb = Entry(frame_pb, textvariable=valuepb, width=30)
boutonpb = Button(frame_pb, text="Lancer la simulation", command=fin)
boutonpb.bind("<Return>", fin)
labelpb.pack()
entreepb.pack()
boutonpb.pack()


## label d'erreur
label_error2 = Label(fenetre, text = "Veuillez entrer une valeur entre 0 et 1")
label_error1 = Label(fenetre, text = "Veuillez entrer une valeur numérique")
label_error3 = Label(fenetre, text = "Veuillez renseigner une valeur inférieure au nombre total de noeuds")
label_error4 = Label(fenetre, text = "Un des noeuds sélectionné a déjà été choisi comme infecté par A")
label_error7 = Label(fenetre, text = "La liste suggérée contient des doublons")
label_error8 = Label(fenetre, text = "Augmenter la probabilité d'activation, le graphe n'est pas connexe") 
label_error9 = Label(fenetre, text = "Le degré choisi ne peut pas excéder la taille du graphe")
label_error10 = Label(fenetre, text = "Le nombre de noeuds infectés choisi ne peut pas respecter la taille du graphe")
label_error12 = Label(fenetre, text = "Le fichier sélectionné ne respecte pas le format 'gexf'")

fenetre.mainloop()



################### Lancement de la simulation ####################

q = animated_graph.animator(G)
       
t_debut = time.time()

competing_propag.unicast_simple_competing_propagation(G, infectes_a, infectes_b, p_inf_a, p_inf_b, q)

t_fin = time.time()
print("TEMPS = ", t_fin - t_debut)


### Affichage / Animation
positions = nx.spring_layout(G)  # positions for all nodes
fig = plt.figure(figsize=(10, 10))
gs = gridspec.GridSpec(2, 2, height_ratios=[3,2])
ax = fig.add_subplot(gs[:-1, :])
ax.clear()
s1 = plt.scatter([], [], c="lightgray", marker='o')
s2 = plt.scatter([], [], c="red", marker='o')
s3 = plt.scatter([], [], c="blue", marker='o')

compt = 0

def update(frame):
    ax.clear()
    ax.set_title("Competing malware", fontweight='bold', fontsize=10, y=0)
    ax.legend((s1, s2, s3), ('susceptible', 'infected by a', 'infected by b'), loc='best')
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
                                         interval=1000,
                                         repeat=False)


# Draw horizontal line
line = plt.Line2D([0, 1], [0.45, 0.45], color="black", linewidth=1, transform=fig.transFigure, figure=fig)
fig.lines.append(line)

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
line1 = ax2.plot(x1[0], l1[0], color='red',label='infected by a')[0]
line2 = ax2.plot(x1[0], l2[0], color='black',label='susceptible')[0]
line3 = ax2.plot(x1[0], l3[0], color='blue',label='infected by b')[0]
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
                                          interval = 1,
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
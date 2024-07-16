###################################################################
############################ Imports ##############################
###################################################################
import time
from matplotlib.animation import writers
import attack_app2
import animation_attack
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
from tkinter import filedialog
import os

#####################################################################
######################## Variables globales #########################
#####################################################################


spinboxes_inf = []
spinboxes_res = []
choicevideo = ""
G = nx.empty_graph(n=0, create_using=None)
nb_noeuds = 0 
nb_inf = 0 
nb_res = 0 
infectes = []
resistants = []
nb_h = 0 
nb_hs = 0
alpha = 0    ## probabilité de I vers S
rho = 0     ## probabilité de S vers R 
propor_propa = 0 
choix_propa = ""



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
            debut_sr()
        else:
            label_error12.pack()


################################
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
        debut_sr() 
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
            debut_sr()
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



def debut_sr(event=None):
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
                        labelsr.pack()
                        entreesr.pack()
                        entreesr.focus_set()
                        boutonsr.pack()
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
                    labelsr.pack()
                    entreesr.pack()
                    entreesr.focus_set()
                    boutonsr.pack()
            except ValueError: 
                label_error1.pack() 
                entree2.focus_set()

        case _:
            ## création des nouveaux widgets
            labelsr.pack()
            entreesr.pack()
            entreesr.focus_set()
            boutonsr.pack()
            




def proba_sr(event=None):
    label_error1.pack_forget()
    label_error2.pack_forget()
    global rho
    string_sr = valuesr.get()
    try: 
        p_sr = float(string_sr)
        if ((p_sr > 1) or (p_sr < 0)):
            label_error2.pack()
            entreesr.focus_set()
        else:
            rho = p_sr
            ## affichage
            labelsr.pack_forget()
            entreesr.pack_forget()
            boutonsr.pack_forget()
            labelis.pack()
            entreeis.pack()
            entreeis.focus_set()
            boutonis.pack()
           

    except ValueError:
        label_error1.pack()
        entreesr.focus_set()
    


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
           # plt.show(block=False)
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
    global nb_inf
    choix = snbm.get()
    choix_int = int(choix)
    if (choix_int > G.number_of_nodes()):
        label_error3.pack()
        snbm.focus_set()
    else: 
        nb_inf = choix_int ## maj valeur
        ### affichage
        label_error3.pack_forget()
        labelnbm.pack_forget()
        snbm.pack_forget()
        boutonnbm.pack_forget()
        if nb_inf > 0:
            ## création d'une nouvelle fenêtre pour les choix des noeuds
            frame_s_m.pack(expand=True)
            sc_v.pack(side='right', fill=Y)
            l = Label(frame_s_m, text="Entrer les indices des noeuds infectés")
            l.pack()
            canv.pack(expand=True)
            canv.create_window((0,0), window=framespinm, anchor=CENTER)
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
        frame_s_m.destroy()
        labelnbr.pack()
        snbr.pack()
        boutonnbr.pack()
        boutonnbr.focus_set()
    elif val_ok:
        label_error7.pack()
    else : 
        label_error3.pack()


def citer_resistants(event=None):
    global nb_res
    choix = snbr.get()
    choix_int = int(choix)
    if (choix_int > G.number_of_nodes() - nb_inf):
        label_error10.pack()
    else: 
        nb_res = choix_int
        ###
        labelnbr.pack_forget()
        snbr.pack_forget()
        boutonnbr.pack_forget()
        if nb_res >0:
            frame_s_r.pack(expand=True)
            sc_v2.pack(side='right', fill=Y)
            l = Label(frame_s_r, text="Entrer les indices des noeuds résistants")
            l.pack()
            canvb.pack(expand=True)
            canvb.create_window((0,0), window=framespinr, anchor=CENTER)
            framespinr.bind("<Configure>", scroll_fun2)
            for i in range(int(choix)):
                temp_l = Label(framespinr, text="Indice du noeud résistant %s" % str(i+1))
                temp_l.pack()
                temp_spin = Spinbox(framespinr, from_=0, to=500)
                spinboxes_res.append(temp_spin)
                temp_spin.pack()
            boutoncm = Button(framespinr, text="Valider", command=nb_hp)
            boutoncm.bind("<Return>", nb_hp)
            boutoncm.pack()
            boutoncm.focus_set()
        else:
            nb_hp()


def nb_hp(event=None): 
    label_error3.pack_forget()
    label_error4.pack_forget()
    label_error7.pack_forget()
    label_error10.pack_forget()
    liste_valeurs = recup_liste_spin(spinboxes_res)
    val_ok = all(v < G.number_of_nodes() for v in liste_valeurs)
    non_inf = all((v not in infectes) for v in liste_valeurs)
    if val_ok and non_inf and pas_de_doublon(liste_valeurs):
        resistants.extend(liste_valeurs)
        frame_s_r.destroy()
        labelhp.pack()
        shp.pack()
        boutonhp.pack()
        boutonhp.focus_set()
    elif val_ok and non_inf:
        label_error7.pack()
    elif val_ok:
        label_error4.pack()
    else:
        label_error3.pack()



def nb_hps(event=None): 
    global G
    global nb_h
    val = shp.get()
    val_int = int(val)
    if (val_int > G.number_of_edges()):
        label_error6.pack()
    else:
        nb_h = val_int
        labelhp.pack_forget()
        shp.pack_forget()
        boutonhp.pack_forget()
        label_error6.pack_forget()
        if nb_h == 0:
            labelts.pack()
            boutonts1.pack()
            boutonts2.pack()
            boutontsv.pack()
            boutontsv.focus_set()
        else:
            labelhps.pack()
            shps.pack()
            boutonhps.pack()
            boutonhps.focus_set()
        


def choix_type_strat(event=None): 
    global nb_hs
    global nb_h
    val = shps.get()
    val_int = int(val)
    if (val_int > nb_h):
        label_error5.pack()
    else:
        nb_hs = val_int
        label_error5.pack_forget()
        labelhps.pack_forget()
        shps.pack_forget()
        boutonhps.pack_forget()
        labelts.pack()
        boutonts1.pack()
        boutonts2.pack()
        boutontsv.pack()
        boutontsv.focus_set()


def choix_strat(event=None):
    val = valuets.get()
    if val not in ["1", "2"]:
        show_message()
    else: 
        labelts.pack_forget()
        boutonts1.pack_forget()
        boutonts2.pack_forget()
        boutontsv.pack_forget()
        if val =="1":
            labels.pack()
            boutons1.pack()
            boutons2.pack()
            label_prop.pack()
            entreestrat.pack()
            boutons3.pack()
            boutonsv.pack()
            boutonsv.focus_set()
        else:
            labels.pack()
            boutons4.pack()
            boutons5.pack()
            boutons6.pack()
            boutonsv.pack()
            boutonsv.focus_set()


def fin(event=None):
    plt.close(fig1)
    global choix_propa
    global propor_propa

    label_error1.pack_forget()
    label_error2.pack_forget()

    choix_strategie = values.get()
    prop = value_strat.get()

    if choix_strategie not in ["1", "2", "3","4","5","6"]:
        show_message()
    else:
        choix_propa = choix_strategie
        match choix_propa: 
            case "2" : 
                try: 
                    fprop = float(prop)
                    if ((fprop > 1) or (fprop < 0)): 
                        label_error2.pack()
                    else:
                        propor_propa = fprop
                        fenetre.destroy()
                except ValueError:
                        label_error1.pack()
            case _:
                fenetre.destroy()






#####################################################################
############################# Composants ############################
#####################################################################


fenetre = Tk()
fenetre.geometry("500x500")
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
bouton11=Button(fenetre, text="Valider", command=debut_sr)
bouton11.bind("<Return>", debut_sr)


## config small-world

label6 = Label(fenetre, text="Entrer le degré initial de chacun des sommets")
value5 = StringVar() 
value5.set("")
entree2 = Entry(fenetre, textvariable=value5, width=30)
label7 = Label(fenetre, text="Entrer la probabilité de modifier chacune des arêtes")
value6 = StringVar() 
value6.set("")
entree3 = Entry(fenetre, textvariable=value6, width=30)
bouton12=Button(fenetre, text="Valider", command=debut_sr)
bouton12.bind("<Return>", debut_sr)

## proba S -> R

labelsr = Label(fenetre, text="Entrer la probabilité qu'un noeud passe de l'état S à R")
valuesr = StringVar()
valuesr.set("")
entreesr = Entry(fenetre, textvariable=valuesr, width=30)
boutonsr = Button(fenetre, text="Valider", command=proba_sr)
boutonsr.bind("<Return>", proba_sr)

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
frame_s_m = Frame(fenetre)
canv = Canvas(frame_s_m)
framespinm = Frame(canv)
sc_v = Scrollbar(frame_s_m, orient='vertical', command = canv.yview)
canv.configure(yscrollcommand=sc_v.set)


## nb noeuds résistants

labelnbr = Label(fenetre, text="Entrer le nombre de noeuds résistants au début de la simulation")
snbr = Spinbox(fenetre, from_=0, to=500)
boutonnbr = Button(fenetre, text="Valider", command=citer_resistants)
boutonnbr.bind("<Return>", citer_resistants)

## lesquels
frame_s_r = Frame(fenetre)
canvb = Canvas(frame_s_r)
framespinr = Frame(canvb)
sc_v2 = Scrollbar(frame_s_r, orient='vertical', command = canvb.yview)
canvb.configure(yscrollcommand=sc_v2.set)

## nb honeypots

labelhp = Label(fenetre, text="Entrer le nombre de honeypots")
shp = Spinbox(fenetre, from_=0, to=500)
boutonhp = Button(fenetre, text="Valider", command=nb_hps)
boutonhp.bind("<Return>", nb_hps)

## nb smart honeypots

labelhps = Label(fenetre, text="Combien de ces honeypots adopteront la stratégie intelligente ? \n Les autres honeypots adopteront la stratégie naïve")
shps = Spinbox(fenetre, from_=0, to=500)
boutonhps = Button(fenetre, text="Valider", command=choix_type_strat)
boutonhps.bind("<Return>", choix_type_strat)


## choix du type de stratégie
labelts = Label(fenetre, text="Choisir le type de stratégie souhaité")
valuets = StringVar()
valuets.set("")
boutonts1 = Radiobutton(fenetre, text="Utiliser une stratégie de propagation basique", variable = valuets, value=1)
boutonts2 = Radiobutton(fenetre, text= "Utiliser une stratégie de propagation qui priorise les noeuds de haut degré", variable=valuets, value=2)
boutonts1.bind("<Return>", activation_radio)
boutonts2.bind("<Return>", activation_radio)
boutontsv = Button(fenetre, text = "Valider", command=choix_strat) 
boutontsv.bind("<Return>", choix_strat)

## choix de la stratégie

labels = Label(fenetre, text="Choisir la stratégie de propagation")
values = StringVar()
values.set("")
value_strat = StringVar()
value_strat.set("")
boutons1 = Radiobutton(fenetre, text="Propagation unicast : un pour un \n(chaque noeud infecté infecte un de ses voisins aléatoirement)", variable=values, value=1)
boutons2 = Radiobutton(fenetre, text="Propagation multicast : proportion à définir \n(chaque noeud infecté infecte une proportion de ses voisins)", variable=values, value=2)
label_prop = Label(fenetre, text= "Entrer la proportion de voisins infectés")
boutons3 = Radiobutton(fenetre, text="Propagation broadcast : un pour tous \n(chaque noeud infecté infecte la totalité de ses voisins)", variable=values, value=3)
boutons4 = Radiobutton(fenetre, text=" Propagation propagation_deterministic_smart : un pour un \n(chaque noeud infecté infecte son voisin de plus grand degré)", variable=values, value=4)
boutons5 = Radiobutton(fenetre, text="Propagation propagation_probabilistic_smart \n(chaque noeud infecté infecte tous ses voisins de plus grand degré et une proportion des autres)", variable=values, value=5)
boutons6 = Radiobutton(fenetre, text=" Propagation multicast_smart : un pour tous les noeuds de plus grand degré \n(chaque noeud infecté infecte tous ses voisins de plus grand degré)", variable=values, value=6)
boutons1.bind("<Return>", activation_radio)
boutons2.bind("<Return>", activation_radio)
boutons3.bind("<Return>", activation_radio)
boutons4.bind("<Return>", activation_radio)
boutons5.bind("<Return>", activation_radio)
boutons6.bind("<Return>", activation_radio)
entreestrat = Entry(fenetre, textvariable=value_strat, width=30)
boutonsv = Button(fenetre, text="Valider", command=fin)
boutonsv.bind("<Return>", fin)

## label d'erreur
label_error2 = Label(fenetre, text = "Veuillez entrer une valeur entre 0 et 1")
label_error1 = Label(fenetre, text = "Veuillez entrer une valeur numérique")
label_error3 = Label(fenetre, text = "Veuillez renseigner une valeur inférieure au nombre total de noeuds")
label_error4 = Label(fenetre, text = "Un des noeuds choisis a déjà été choisi comme infecté")
label_error5 = Label(fenetre, text = "Le nombre de honeypots smarts ne peut pas être supérieur au nombre de honeypots total")
label_error6 = Label(fenetre, text = "Le nombre de Honeypots/IDS choisi dépasse le nombre d'arêtes total dans le graphe")
label_error7 = Label(fenetre, text = "La liste suggérée contient des doublons")
label_error8 = Label(fenetre, text = "Augmenter la probabilité d'activation, le graphe n'est pas connexe") 
label_error9 = Label(fenetre, text = "Le degré choisi ne peut pas excéder la taille du graphe")
label_error10 = Label(fenetre, text = "Le nombre de noeuds résistants choisi ne peut pas respecter la taille du graphe")
label_error12 = Label(fenetre, text = "Le fichier sélectionné ne respecte pas le format 'gexf'")


fenetre.mainloop()


###################################################################
################### Lancement de la simulation ####################
###################################################################

q = animation_attack.queue(G)       
t_debut = time.time()
match choix_propa:

    case "1":
        attack_app2.propagation_unicast(infectes, G, q, resistants, rho, alpha, nb_h, nb_hs)

    case "2":
        attack_app2.propagation_probability(infectes, G, q, resistants, rho, alpha, nb_h, propor_propa, nb_hs)

    case "3":
        attack_app2.propagation_broadcast(infectes, G, q, resistants, rho, alpha, nb_h, nb_hs)
        
    case "4":
        attack_app2.propagation_deterministic_smart(infectes, G, q, resistants, rho, alpha, nb_h, nb_hs)

    case "5":
        attack_app2.propagation_probabilistic_smart(infectes, G, q, resistants, rho, alpha, nb_h, nb_hs)

    case "6":
        attack_app2.propagation_broadcast_smart(infectes, G, q, resistants, rho, alpha, nb_h, nb_hs)

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
s1 = plt.scatter([], [], c="royalblue", marker='o')
s2 = plt.scatter([], [], c="red", marker='o')
s3 = plt.scatter([], [], c="gainsboro", marker='o')

compt = 0


def update(frame):
    ax.clear()
    ax.set_title("Virus propagation", fontweight='bold', fontsize=10, y=0)
    ax.legend((s1, s2, s3), ('susceptible', 'infected', 'resistant'), loc='best')
    nx.draw(
    G,
    pos=positions,
    ax=ax,
    node_size=250,
    with_labels=True,
    font_size=10,
    node_color=q.animation['colors'][frame],
    edge_color=q.animation['colors_edge'][frame],
    width=q.animation['widths'][frame])
	

ani = matplotlib.animation.FuncAnimation(fig,
                                         update,
                                         frames=len(q.animation['colors']),
                                         interval=500,
                                         repeat=False)


# Draw horizontal line
line = plt.Line2D([0, 1], [0.45, 0.45], color="black", linewidth=1, transform=fig.transFigure, figure=fig)
fig.lines.append(line)

ax2 = fig.add_subplot(gs[-1, :])


l1,l2,l3 = q.step_return()
plt.suptitle( 'Attack-Defense model')


x1, y1 ,y2, y3 = [], [], [], []
plt.grid( which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid( which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.xlabel('Time (step)')
plt.ylabel('Population (Individual)')


for n in  range(len(l1)) :
	x1.append(n)

y1 = l1

ax2.plot(x1, l2, color="blue", label='susceptible') 
ax2.plot(x1, l1, color="red", label='infected') 
ax2.plot(x1, l3, color="black",label='resistant') 
ax2.set_title("Evolution of the populations across time", fontweight='bold', fontsize=10)

plt.legend()


plt.tight_layout()


if choicevideo ==  "1" : #Uniquement si ffmpeg est installé
    Writer = writers['ffmpeg']
    writer = Writer(
        fps=2,
        metadata=dict(artist="oumaima diami", title = "AnimationPlt"),
        bitrate=8000)

    ani.save("AnimationPlt.mp4", writer=writer)
    HTML(ani.to_html5_video())

    plt.show()
else :

    plt.show()
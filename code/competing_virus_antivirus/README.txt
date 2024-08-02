Ce répertoire contient les codes nécessaires pour la simulation d'un virus en concurrence avec un antivirus. Il contient les fichiers suivants : 

- "animated_graph.py" : fichier pour l'animation des simulations
- "app_antivirus.py" : fichier pour lancer l'application classique virus/antivirus
- "app_antivirus_4.py" : fichier pour lancer l'application virus/antivirus avec l'affichage de tous les couples de stratégies
- "graph_type.py" : fichier pour générer les différents types de graphes
- "virus_antivirus_propagation.py" : fichier pour générer les différentes simulations

- Ce répertoire contient également un autre répertoire "game_theory" contenant les codes pour les jeux compétitifs. Ce deuxième répertoire contient : 
	- "animated_graph.py" : pour l'animation 
	- "app_sim" : pour lancer l'application, code modifié pour le jeu
	- "Delta_time_fun.py" : fichier de définition de la fonction Delta
	- "game.py": fichier de génération de simulations sans l'aspect graphique pour la génération de données
	- "game_sim.py" : fichier de génération des simulations avec l'aspect graphique, appelé par "app_sim.py"
	- "graph_generator.py" : générateur de graphe (il faut modifier les paramètres et le nom du graphe dans le code) 
	- "graph_type.py" : fichier de génération des différents types de graphes
	- "simu.py", "simu copy.py", "simu2.py" : fichier de générations des simulations avec différents paramètres
	- "display_cost_fun.ipynb" : notebook pour la visualisation de la fonction de coût liée au jeu
	- "res_visu.ipynb", "res_visu_copy.ipynb", "res_visu_cumul.ipynb" : notebooks pour la visualisation des résultats du jeu
	avec différentes fonctions de coûts et paramètres
	- Ce répertoire contient un autre dossier "res_simu", ce dossier contient les résultats des simulations ainsi qu'un index répertoriant les différents fichiers résultats

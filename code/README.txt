Ce répertoire contient les codes du projet, il est lui même constitué d'autres répertoires, on fait ici un listing des fichiers et répertoires présents : 

- Dans le dossier principal, il y a les fichiers relatifs aux codes du simulateur avec les honeypots/IDS, ainsi on retrouve : 
	"animation_attack.py" : code de l'animation 
	"app_graphique.py" : application graphique permettant de lancer le simulateur et l'animation 
	"app1.py" : application en ligne de commande permettant de lancer le simulateur et l'animation
	"attack_app.py" : code de la simulation de l'ancienne stagiaire, appelé par app1
	"attack_app2.py" : code de la simulation modifié et un peu "optimisé", appelé par app_graphique
	"attack_app2_gen_game.py" : code de la simulation sans l'aspect graphique pour la génération de données de simulations
	"game_sim.py" : fichier de lancement de génération de données pour le jeu 
	"graph_generator.py" : fichier permettant de générer un graphe (il faut modifier le nom et les paramètres)
	"graph_type.py" : fichier pour générer les différents types de graphes
	"graph_visualizer.py" : fichier pour la visualisation de graphes déjà créés
 	"game_result_visualisation.ipynb" : fichier pour la visualisation des résultats du jeu avec les honeypots
	"readme.pdf" : fichier readme pour l'application en ligne de commande écrit par l'ancienne stagiaire
	Des fichiers ".gexf" qui sont des graphes
	Des fichiers "résultats" contenant les résultats de simulation pour le jeu avec les honeypots
- Le dossier principal contient 3 autres répertoires : 
	"competing_virus_antivirus" : contient les codes de la simulation de l'opposition entre la diffusion d'un virus et d'un antivirus
	"competing_viruses" : contient les codes de la simulation de deux virus concurrents
	"ia" : contient les codes sur les méthodes de machine learning utilisés pour la prédiction des métriques de simulation
- Chacun de ces 3 répertoires contient un fichier README.txt pour expliquer les codes qui y sont présents.
Ce répertoire contient les codes nécessaires pour la prédiction des métriques de simulation avec des outils de machine learning. Il contient : 

- "attack_app2_gen.py" : fichier pour les simulations sans l'aspect graphique pour la génération de données
- "graph_parallel_generator.py" : fichier pour la génération de données en parallèle (avec un graphe différent pour chaque simulation)
- "graph_type.py" : fichier pour la génération des différents types de graphes
- "reseau.py" : fichier py du réseau avec un graphe différent par simulation (obsolète avec la présence du notebook)
- "reseau_single_graphe.py" : fichier py du réseau avec un seul graphe pour toutes les simulations (obsolète avec la présence du notebook)
- "single_graph_parallel_generator.py" : fichier pour la génération de données en parallèle (même graphe pour toutes les simulations)
- "notebook_single_graphe.ipynb" : notebook du réseau avec un seul graphe pour toutes les simulations (se modifie rapidement pour un graphe variable)
- "svr_single_graphe.ipynb" : notebook pour la svr avec un seul graphe pour toutes les simulations (se modifie rapidement pour un graphe variable)
- des fichiers ".gexf" qui sont des graphes utilisés pour la génération de données
- un répertoire "résultats" contenant les résultats des générations de données avec un index
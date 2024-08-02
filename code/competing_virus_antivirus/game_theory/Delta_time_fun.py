#####################################################################################################################
### Fonction qui retourne le Delta = temps de R&D de l'antivirus en fonction de K, coût investi dans la recherche ###
#####################################################################################################################

def delta_fun(K):
    if K == 0: 
        return(500)
    else:
        return int(200/K)
import pandas as pd

def calculer_moyennes_mensuelles(compteurs):
    """
    Calcule la moyenne des intensités mensuelles pour chaque compteur et ajoute une colonne "mean_total".
    Exclut les moyennes pour "Compteur Vélo Gerhardt".

    Arguments :
        compteurs : DataFrame contenant les données des compteurs, incluant des colonnes 
                                   avec les moyennes mensuelles au format "mean_<mois>".

    Retourne :
        tuple : 
            - compteurs : Le DataFrame mis à jour avec une colonne "mean_total".
            - mean_columns : Liste des noms des colonnes correspondant aux moyennes mensuelles utilisées dans le calcul.
    """
    mean_columns = [col for col in compteurs.columns if col.startswith("mean_")] 
    compteurs['mean_total'] = compteurs[mean_columns].mean(axis=1)
    
    # Gestion de la ligne pour "Compteur Vélo Gerhardt"
    ligne_gerhardt = compteurs["Nom du com"] == "Compteur Vélo Gerhardt"
    compteurs.loc[ligne_gerhardt, mean_columns] = None

    return compteurs, mean_columns

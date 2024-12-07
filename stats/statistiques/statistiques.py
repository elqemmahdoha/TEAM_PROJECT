import pandas as pd

def calculer_moyennes_mensuelles(compteurs):
    """Calcule la moyenne de chaque colonne des intensités mensuelles et ajoute à 'mean_total'."""
    mean_columns = [col for col in compteurs.columns if col.startswith("mean_")] 
    compteurs['mean_total'] = compteurs[mean_columns].mean(axis=1)
    
    # Gestion de la ligne pour "Compteur Vélo Gerhardt"
    ligne_gerhardt = compteurs["Nom du com"] == "Compteur Vélo Gerhardt"
    compteurs.loc[ligne_gerhardt, mean_columns] = None

    return compteurs, mean_columns

import os
import pandas as pd
from .traitement_donnees import charger_compteurs, charger_intensites_par_mois
from .statistiques import calculer_moyennes_mensuelles
from .visualisation import creer_figure_polaire, creer_figure_intensite_moyenne

def main(): 
    # Créer un sous-répertoire pour les figures
    dossier_destination = "docs\\figures"
    os.makedirs(dossier_destination, exist_ok=True)

    chemin_average_intensity = os.path.join(dossier_destination, "average_intensity_month.html")
    chemin_polar_figure = os.path.join(dossier_destination, "polar_figure.html")

    # Charger les compteurs
    compteurs = charger_compteurs("data/video/ecocompt/GeolocCompteurs.geojson")

    # Plage de dates
    date_debut = pd.to_datetime("2024-03-01").date()
    date_fin = pd.to_datetime("2024-10-31").date()

    # Extraire les intensités par mois
    compteurs = charger_intensites_par_mois(compteurs, date_debut, date_fin)

    # Calculer les moyennes mensuelles
    compteurs, mean_columns = calculer_moyennes_mensuelles(compteurs)

    # Calculer les moyennes
    mean_values = compteurs[mean_columns].apply(pd.to_numeric, errors='coerce').mean()

    # Préparer le tableau des moyennes
    month_names = {
        "mean_03": "Mars", "mean_04": "Avril", "mean_05": "Mai",
        "mean_06": "Juin", "mean_07": "Juillet", "mean_08": "Août",
        "mean_09": "Septembre", "mean_10": "Octobre"
    }

    tableau_moyennes = pd.DataFrame({
        "Month": [month_names[col] for col in mean_columns],
        "Average Intensity": mean_values.values
    })

    # Trier les compteurs par intensité totale
    topcompteurs = compteurs[['Nom du com', 'mean_total'] + mean_columns].sort_values(by='mean_total', ascending=False).head(10)
    topcompteurs.rename(columns=month_names, inplace=True)

    # Préparer les données pour la visualisation polaire
    polar_data = topcompteurs.melt(id_vars=['Nom du com'], value_vars=list(month_names.values()), 
                                   var_name='Month', value_name='Intensity')

    # Créer et enregistrer les graphiques
    creer_figure_polaire(polar_data, chemin_polar_figure)
    creer_figure_intensite_moyenne(tableau_moyennes, chemin_average_intensity)

if __name__ == "__main__":
    main()
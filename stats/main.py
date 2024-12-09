import os
import pandas as pd
import time
from .traitement_donnees import charger_compteurs, charger_intensites_par_mois
from .statistiques import calculer_moyennes_mensuelles
from .visualisation import creer_figure_polaire, creer_figure_intensite_moyenne

def main():
    """
    Script principal pour l'analyse des données des compteurs de vélos et la génération de visualisations.

    Ce script charge les données des compteurs de vélos depuis un fichier GeoJSON, extrait les intensités mensuelles de passage pour une période spécifiée, calcule les moyennes mensuelles et génère des visualisations interactives des intensités. Les graphiques générés sont sauvegardés sous forme de fichiers HTML.

    Le processus inclut les étapes suivantes :
    1. Création d'un sous-répertoire pour sauvegarder les figures générées.
    2. Chargement des données des compteurs de vélos depuis un fichier GeoJSON.
    3. Extraction des intensités de passage pour chaque mois sur la période spécifiée.
    4. Calcul des moyennes mensuelles d'intensité pour chaque compteur.
    5. Préparation des données nécessaires à la génération des graphiques :
    - Moyennes mensuelles d'intensité pour chaque mois de la période.
    - Classement des compteurs par intensité totale, et sélection des 10 premiers.
    6. Création de deux visualisations :
    - Un graphique polaire des intensités mensuelles moyennes pour chaque compteur.
    - Un graphique des intensités moyennes mensuelles globales.
    7. Sauvegarde des graphiques sous forme de fichiers HTML dans un dossier dédié.

    Modules utilisés :
    - `traitement_donnees`: Pour charger les données des compteurs et extraire les intensités mensuelles.
    - `statistiques`: Pour calculer les moyennes mensuelles d'intensité.
    - `visualisation`: Pour générer les graphiques interactifs des intensités moyennes.
    - `pandas`: Pour la manipulation des données et le calcul des moyennes.
    - `os`: Pour la gestion des répertoires et des chemins de fichiers.

    Temps d'exécution : environ 10 secondes.

    """
 
    # Créer un sous-répertoire pour les figures
    dossier_destination = "docs\\figures"
    os.makedirs(dossier_destination, exist_ok=True)

    chemin_average_intensity = os.path.join(dossier_destination, "average_intensity_month.html")
    chemin_polar_figure = os.path.join(dossier_destination, "polar_figure.html")

    # Charger les compteurs
    compteurs = charger_compteurs("data/files/MMM_MMM_GeolocCompteurs_sorted.geojson")

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
    start = time.time()
    main()
    end = time.time()
    print(f"Temps : {end - start:.5f} s")  
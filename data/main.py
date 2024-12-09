import time
from .fetch_data import fetch_all_files
from .tri_csv import charger_csv, corriger_encodage, filtrer_donnees, sauvegarder_csv 
from .tri_json import filtre_geojson, filtrer_fichiers_par_numeros, copier_et_nettoyer_fichiers, add_stations

def main():
    """
    Fonction principale pour : 
        - scraper la page de données de Montpellier Méditerranée Métropole 
        - charger les numéros de série des compteurs, filtrer les fichiers archive_json correspondants, et les copier après nettoyage.
        - charger, corriger, filtrer et sauvegarder le fichier CSV des courses Velomagg.

    """
    fetch_all_files()

    # Chemins des fichiers 
    geojson_path = 'data\\files\\MMM_MMM_GeolocCompteurs.geojson'
    dossier_fichiers = 'data\\files'
    dossier_destination = 'data\\files\\filtered'

    input_file = 'data\\files\\TAM_MMM_CoursesVelomagg.csv'
    output_file = 'data\\files\\filtered\\CoursesVelomagg_filtre.csv'

    # Date du filtre 
    date_debut = "2024-08-01"

    # Ajouter des stations Velomagg 
    file_path = "data\\files\\MMM_MMM_Velomagg.json"
    add_stations(file_path)

    # Charger les numéros de série à partir du fichier GeoJSON
    numeros_serie_geojson = filtre_geojson(geojson_path)
    
    # Filtrer les fichiers à partir des numéros de série
    fichiers_selectionnes = filtrer_fichiers_par_numeros(dossier_fichiers, numeros_serie_geojson)

    # Copier et nettoyer les fichiers
    copier_et_nettoyer_fichiers(fichiers_selectionnes, dossier_fichiers, dossier_destination)

    # Charger le fichier CSV
    df = charger_csv(input_file)

    # Corriger les erreurs d'encodage
    df = corriger_encodage(df)

    # Filtrer les données
    df_filtered = filtrer_donnees(df, date_debut)

    # Sauvegarder le fichier filtré
    sauvegarder_csv(df_filtered, output_file)
    print(f"Le fichier filtré a été sauvegardé sous {output_file}")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Temps : {end - start:.5f} s")
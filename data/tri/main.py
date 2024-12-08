import time
from .tri_csv import charger_csv, correct_encoding, corriger_encodage, filtrer_donnees, sauvegarder_csv 
from .tri_json import charger_numeros_serie_geojson, filtrer_fichiers_par_numeros, copier_et_nettoyer_fichiers

def main():
    """
    Fonction principale pour : 
        - charger les numéros de série des compteurs, filtrer les fichiers archive_json correspondants, et les copier après nettoyage.
        - charger, corriger, filtrer et sauvegarder le fichier CSV des courses Velomagg.

    """
    geojson_path = 'data\\video\\ecocompt\\GeolocCompteurs.geojson'
    dossier_fichiers = 'data\\video\\ecocompt'
    dossier_destination = 'data\\video\\ecocompt\\filtered'

    input_file = 'data\\video\\courses\\TAM_MMM_CoursesVelomagg.csv'
    output_file = 'data\\video\\courses\\CoursesVelomagg_filtre.csv'
    date_debut = "2024-08-01"

    # Charger les numéros de série à partir du fichier GeoJSON
    numeros_serie_geojson = charger_numeros_serie_geojson(geojson_path)

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
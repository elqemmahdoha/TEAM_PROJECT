import os
import json
import shutil

def charger_numeros_serie_geojson(geojson_path: str) -> set:
    """
    Charge le fichier GeoJSON et extrait les numéros de série des compteurs.
    
    Arguments:
        geojson_path (str): Chemin vers le fichier GeoJSON contenant les données des compteurs.

    Retourne:
        set: Un ensemble des numéros de série extraits du fichier GeoJSON.
    """
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Extraire les numéros de série prioritaires
    numeros_serie_geojson = set(
        feature['properties'].get('N° Sér_1') or feature['properties'].get('N° Série')
        for feature in geojson_data['features']
        if feature['properties'].get('N° Sér_1') or feature['properties'].get('N° Série')
    )

    # Supprimer les None (cas où aucune clé valide n'était présente)
    numeros_serie_geojson.discard(None)
    
    return numeros_serie_geojson

def filtrer_fichiers_par_numeros(dossier_fichiers: str, numeros_serie_geojson: set) -> list:
    """
    Filtre les fichiers dans le dossier donné en fonction des numéros de série extraits du fichier GeoJSON.

    Arguments:
        dossier_fichiers (str): Dossier contenant les fichiers à filtrer.
        numeros_serie_geojson (set): Ensemble des numéros de série à rechercher dans les fichiers.

    Retourne:
        list: Liste des fichiers sélectionnés qui contiennent les numéros de série extraits.
    """
    fichiers = os.listdir(dossier_fichiers)
    fichiers_selectionnes = [fichier for fichier in fichiers if any(numero in fichier for numero in numeros_serie_geojson)]
    
    return fichiers_selectionnes

def copier_et_nettoyer_fichiers(fichiers_selectionnes: list, dossier_fichiers: str, dossier_destination: str):
    """
    Copie les fichiers sélectionnés dans un nouveau dossier et nettoie le contenu des fichiers JSON (supprimer les sauts de ligne inutiles).
    
    Arguments:
        fichiers_selectionnes (list): Liste des fichiers à copier et nettoyer.
        dossier_fichiers (str): Dossier source contenant les fichiers.
        dossier_destination (str): Dossier de destination pour les fichiers copiés et nettoyés.
    """
    os.makedirs(dossier_destination, exist_ok=True)  # Crée le dossier s'il n'existe pas

    for fichier in fichiers_selectionnes:
        chemin_fichier_source = os.path.join(dossier_fichiers, fichier)
        chemin_fichier_destination = os.path.join(dossier_destination, fichier)

        # Copier le fichier
        shutil.copy(chemin_fichier_source, chemin_fichier_destination)

        # Nettoyer le fichier
        with open(chemin_fichier_destination, 'r', encoding='utf-8') as f:
            lignes = f.read()  # Lire tout le fichier comme une chaîne

        # Correction des objets JSON collés (ajouter une nouvelle ligne entre les objets JSON)
        lignes_corrigees = lignes.replace("}{", "}\n{")
        lignes_corrigees = "\n".join([ligne.strip() for ligne in lignes_corrigees.splitlines() if ligne.strip()])

        with open(chemin_fichier_destination, 'w', encoding='utf-8') as f:
            f.write(lignes_corrigees)  # Réécrire le fichier sans les lignes vides et avec les retours à la ligne corrigés

        print(f"Fichier '{fichier}' nettoyé et copié dans '{dossier_destination}'")
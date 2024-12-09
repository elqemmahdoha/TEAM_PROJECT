import os
import json
import shutil

def filtre_geojson(geojson_path: str) -> list:
    """
    Charge le fichier GeoJSON, filtre et trie les numéros de série des compteurs, puis enregistre le résultat.
    
    Arguments:
        geojson_path (str): Chemin vers le fichier GeoJSON contenant les données des compteurs.
    
    Retourne:
        list: Une liste des numéros de série valides.
    """
    # Liste des numéros de série valides
    numeros_serie_valides = [
        'X2H21070344', 'X2H20063164', 'X2H20063163', 'X2H21070341', 'X2H22104776', 'X2H19070220', 
        'X2H21070350', 'XTH19101158', 'X2H22104768', 'ED223110495', 'X2H22043035', 'XTH24072390', 
        'X2H22104777', 'X2H21070342', 'X2H21111121', 'ED223110497', 'ED223110496', 'X2H22104770', 
        'X2H22104773', 'X2H20104132', 'X2H21070343', 'X2H21111120', 'X2H22043034', 'X2H22104775', 
        'X2H22104769', 'X2H21070345', 'X2H22104774', 'X2H20063161', 'X2H22043033', 'X2H20063162', 
        'X2H21070347', 'ED223110501', 'ED223110500', 'X2H22043029', 'X2H21070348', 'X2H20042633', 
        'X2H21070349'
    ]

    # Chargement du fichier GeoJSON
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Filtrer les caractéristiques (features) selon les numéros de série valides
    filtered_features = [
        feature for feature in geojson_data['features']
        if (feature['properties'].get('N° Sér_1') in numeros_serie_valides) or 
           (feature['properties'].get('N° Série') in numeros_serie_valides)
    ]

    # Trier les caractéristiques (features) par numéro de série
    filtered_features.sort(key=lambda feature: (
        feature['properties'].get('N° Sér_1') or feature['properties'].get('N° Série')
    ))

    # Mettre à jour les données avec les caractéristiques triées
    geojson_data['features'] = filtered_features

    # Créer un nouveau fichier GeoJSON avec les données triées
    new_geojson_path = geojson_path.replace('.geojson', '_sorted.geojson')
    with open(new_geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)

    # Supprimer l'ancien fichier (en toute sécurité)
    os.remove(geojson_path)

    # Retourner la liste des numéros de série valides
    return numeros_serie_valides


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

def add_stations(input_file_path, output_file_path):
    """
    Ajoute des nouvelles entrées de type Feature à un fichier JSON existant
    et enregistre le résultat dans un nouveau fichier.

    Arguments:
        input_file_path (str): Chemin du fichier JSON source.
        output_file_path (str): Chemin du fichier JSON où les données mises à jour seront enregistrées.
    """
    # Nouvelles fonctionnalités à ajouter
    new_features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [3.869217398604767, 43.62842854135043]
            },
            "properties": {
                "nom": "Fac de Lettres",
                "secteur": "",
                "installati": "12 vélos",
                "commune": "MONTPELLIER",
                "numero": 38,
                "type_stati": "sans CB"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [3.871168886060632, 43.63534439935278]
            },
            "properties": {
                "nom": "Vert-Bois",
                "secteur": "",
                "installati": "16 vélos",
                "commune": "MONTPELLIER",
                "numero": 34,
                "type_stati": "sans CB"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [3.8727634196650214, 43.609010705140435]
            },
            "properties": {
                "nom": "Saint-Guilhem - Courreau",
                "secteur": "ligne 4",
                "installati": "8 vélos",
                "commune": "MONTPELLIER",
                "numero": 57,
                "type_stati": "sans CB"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [3.884182597493091, 43.609754007595754]
            },
            "properties": {
                "nom": "Jean de Beins",
                "secteur": "",
                "installati": "16 vélos",
                "commune": "MONTPELLIER",
                "numero": 61,
                "type_stati": "sans CB"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [3.8842150963510873, 43.60137969689591]
            },
            "properties": {
                "nom": "Cité Mion",
                "secteur": "",
                "installati": "8 vélos",
                "commune": "MONTPELLIER",
                "numero": 24,
                "type_stati": "sans CB"
            }
        }
    ]

    # Charger le contenu existant
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Ajouter les nouvelles fonctionnalités
    data["features"].extend(new_features)
    
    # Sauvegarder les modifications dans un nouveau fichier
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Les nouvelles entrées ont été ajoutées et sauvegardées dans {output_file_path}.")

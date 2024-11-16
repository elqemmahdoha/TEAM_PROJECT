import json
import os
import shutil

# Charger le fichier GeoJSON pour obtenir les numéros de série
with open('data\\video\\ecocompt\\GeolocCompteurs.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Extraire tous les numéros de série dans le fichier GeoJSON (priorité à "N° Série 1", puis "N° Série")
numeros_serie_geojson = set(
    feature['properties'].get('N° Sér_1') or feature['properties'].get('N° Série')  # "N° Série 1" en priorité
    for feature in geojson_data['features']
    if feature['properties'].get('N° Sér_1') or feature['properties'].get('N° Série')  # Vérification de la présence d'une clé
)

# Supprimer les None (cas où aucune clé valide n'était présente)
numeros_serie_geojson.discard(None)

# Dossier contenant les fichiers à filtrer
dossier_fichiers = "data\\video\\ecocompt"

# Liste des fichiers dans le dossier
fichiers = os.listdir(dossier_fichiers)

# Filtrer les fichiers dont la partie "ED223110500" (ou similaire) dans le nom correspond aux numéros extraits
fichiers_selectionnes = [fichier for fichier in fichiers if any(numero in fichier for numero in numeros_serie_geojson)]

# Créer un sous-répertoire de destination pour les fichiers filtrés
dossier_destination = "data\\video\\ecocompt\\filtered"
os.makedirs(dossier_destination, exist_ok=True)  # Crée le dossier s'il n'existe pas

# Copier et nettoyer les fichiers sélectionnés
for fichier in fichiers_selectionnes:
    chemin_fichier_source = os.path.join(dossier_fichiers, fichier)
    chemin_fichier_destination = os.path.join(dossier_destination, fichier)

    # Copier le fichier
    shutil.copy(chemin_fichier_source, chemin_fichier_destination)

    # Supprimer les sauts de ligne inutiles et corriger les objets JSON collés
    with open(chemin_fichier_destination, 'r', encoding='utf-8') as f:
        lignes = f.read()  # Lire tout le fichier comme une chaîne

    # Correction des objets JSON collés
    # Trouver les objets JSON collés (il n'y a pas de retour à la ligne entre les objets JSON)
    lignes_corrigees = lignes.replace("}{", "}\n{")  # Insérer un retour à la ligne entre les objets JSON

    # Supprimer les sauts de ligne inutiles et les espaces superflus
    lignes_corrigees = "\n".join([ligne.strip() for ligne in lignes_corrigees.splitlines() if ligne.strip()])

    with open(chemin_fichier_destination, 'w', encoding='utf-8') as f:
        f.write(lignes_corrigees)  # Réécrit le fichier sans les lignes vides et avec les retours à la ligne corrigés

    print(f"Fichier '{fichier}' nettoyé et copié dans '{dossier_destination}'")

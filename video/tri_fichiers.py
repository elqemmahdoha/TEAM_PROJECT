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

# Afficher les numéros de série extraits
print("Numéros de série extraits :")
print(numeros_serie_geojson)

# Dossier contenant les fichiers à filtrer
dossier_fichiers = "data\\video\\ecocompt"

# Liste des fichiers dans le dossier
fichiers = os.listdir(dossier_fichiers)

# Filtrer les fichiers dont la partie "ED223110500" (ou similaire) dans le nom correspond aux numéros extraits
fichiers_selectionnes = [fichier for fichier in fichiers if any(numero in fichier for numero in numeros_serie_geojson)]

# Afficher les fichiers sélectionnés
print("Fichiers sélectionnés:", fichiers_selectionnes)

# Créer un sous-répertoire de destination pour les fichiers filtrés
dossier_destination = "data\\video\\ecocompt\\filtered"
os.makedirs(dossier_destination, exist_ok=True)  # Crée le dossier s'il n'existe pas

# Copier les fichiers sélectionnés dans le sous-répertoire
for fichier in fichiers_selectionnes:
    chemin_fichier_source = os.path.join(dossier_fichiers, fichier)
    chemin_fichier_destination = os.path.join(dossier_destination, fichier)
    
    # Copier le fichier
    shutil.copy(chemin_fichier_source, chemin_fichier_destination)
    #print(f"Fichier '{fichier}' copié dans '{dossier_destination}'")

import json
import os
import shutil

# Charger le fichier GeoJSON pour obtenir les numéros de série
with open('data\ecocompt\GeolocCompteurs.geojson', 'r',encoding='utf-8') as f:
    geojson_data = json.load(f)

# Extraire tous les numéros de série dans le fichier GeoJSON (avec une vérification de la clé)
numeros_serie_geojson = set(
    feature['properties'].get('N° Série', None)  # Utilisation de .get() pour éviter l'erreur
    for feature in geojson_data['features']
    if feature['properties'].get('N° Série')  # S'assurer que 'N° Série' existe avant de l'ajouter
)

# Supprimer les None (cas où la clé 'N° Série' était absente)
numeros_serie_geojson.discard(None)

# Afficher les numéros de série extraits
print("Numéros de série extraits :")
print(numeros_serie_geojson)

# Dossier contenant les fichiers à filtrer
dossier_fichiers = "data\ecocompt"

# Liste des fichiers dans le dossier
fichiers = os.listdir(dossier_fichiers)

# Filtrer les fichiers dont la partie "ED223110500" (ou similaire) dans le nom correspond aux numéros extraits
fichiers_selectionnes = [fichier for fichier in fichiers if any(numero in fichier for numero in numeros_serie_geojson)]

# Afficher les fichiers sélectionnés
print("Fichiers sélectionnés:", fichiers_selectionnes)

# Créer un sous-répertoire de destination pour les fichiers filtrés
dossier_destination = "data\\ecocompt\\fichiers_video"
os.makedirs(dossier_destination, exist_ok=True)  # Crée le dossier s'il n'existe pas

# Copier les fichiers sélectionnés dans le sous-répertoire
for fichier in fichiers_selectionnes:
    chemin_fichier_source = os.path.join(dossier_fichiers, fichier)
    chemin_fichier_destination = os.path.join(dossier_destination, fichier)
    
    # Copier le fichier
    shutil.copy(chemin_fichier_source, chemin_fichier_destination)
    print(f"Fichier '{fichier}' copié dans '{dossier_destination}'")
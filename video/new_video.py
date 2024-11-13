import geopandas as gpd
import osmnx as ox  
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json
import os
from datetime import datetime

# Charger le réseau de rues de Montpellier
montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="bike")

# Charger le fichier GeoJSON contenant les points de comptage
compteurs = gpd.read_file("data/ecocompt/GeolocCompteurs.geojson")

# Charger les données de passages pour chaque compteur en filtrant pour juin
passages = {}
for compteur_id in compteurs.index:
    # Récupérer l'identifiant correct du compteur
    compteur_unique_id = compteurs.loc[compteur_id, 'N° Sér_1'] or compteurs.loc[compteur_id, 'N° Série']
    file_path = f"data/ecocompt/fichiers_video/MMM_EcoCompt_{compteur_unique_id}_archive.json"
    
    if not os.path.exists(file_path):
        print(f"Fichier introuvable pour le compteur {compteur_unique_id}")
        continue  # Passer au compteur suivant si le fichier est introuvable
    
    with open(file_path, 'r') as f:
        for line in f:
            try:
                # Charger chaque ligne comme un objet JSON
                entry = json.loads(line)
                
                # Extraire et traiter la date
                date_str = entry["dateObserved"].split("/")[0]  # Récupérer la première date de l'intervalle
                date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")  # Convertir en objet datetime
                
                # Filtrer pour le mois de juin 2024
                if date.month == 6 and date.year == 2024:
                    intensity = entry["intensity"]
                    # Ajouter l'intensité par date
                    if date not in passages:
                        passages[date] = {}
                    passages[date][compteur_id] = intensity

            except json.JSONDecodeError as e:
                print(f"Erreur de décodage sur la ligne: {line}")
                print(f"Erreur : {e}")

# Extraire et trier les dates de juin
dates = sorted(passages.keys())
print("Dates disponibles pour l'animation :", dates)  # Vérifier les dates

# Vérifier s'il y a des dates disponibles
if not dates:
    print("Aucune date disponible pour l'animation.")
else:
    # Initialisation de la figure
    fig, ax = ox.plot_graph(montpellier_graph, show=False, close=False, node_size=0, edge_color="black", edge_linewidth=0.5, bgcolor="white", figsize=(10, 10))

    # Fonction de mise à jour pour l'animation
    def update(frame):
        ax.clear()
        ox.plot_graph(montpellier_graph, ax=ax, show=False, close=False, node_size=0, edge_color="black", edge_linewidth=0.5, bgcolor="white")
        
        # Date actuelle
        current_date = dates[frame]
        
        # Calculer la taille des marqueurs en fonction de l'intensité
        sizes = []
        for compteur_id in compteurs.index:
            intensity = passages.get(current_date, {}).get(compteur_id, 0)
            sizes.append(intensity / 10)  # Ajustez le facteur de division pour adapter la taille
        
        # Afficher les points de comptage avec une taille dépendante de l'intensité
        compteurs.plot(ax=ax, marker='o', color='red', markersize=sizes, label="Compteurs")
        plt.legend()
        plt.title(f"Date: {current_date.strftime('%Y-%m-%d')}")

    # Créer l'animation
    ani = FuncAnimation(fig, update, frames=len(dates), repeat=False)

    # Sauvegarder la vidéo
    ani.save("intensite_passages_juin.mp4", writer="ffmpeg", fps=2)

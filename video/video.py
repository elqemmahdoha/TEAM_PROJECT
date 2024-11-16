import geopandas as gpd
import json
import osmnx as ox
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Charger le fichier GeoJSON contenant les points de comptage
compteurs = gpd.read_file("data/video/ecocompt/GeolocCompteurs.geojson")

# Extraire les numéros de série des compteurs
compteurs["numero_serie"] = compteurs["N° Sér_1"].fillna(compteurs["N° Série"])

# Initialiser la colonne 'intensities' dans le GeoDataFrame
compteurs["intensities"] = None  # Initialisation de la colonne pour stocker les intensités

# Extraction des intensités de passage des n derniers jours 
n=100
for idx, row in compteurs.iterrows():
    numero_serie = row["numero_serie"]
    if pd.notnull(numero_serie):
        try:
            # Charger le fichier JSON correspondant
            filepath = f"data/video/ecocompt/filtered/MMM_EcoCompt_{numero_serie}_archive.json"
            with open(filepath, 'r', encoding='utf-8') as f:
                # Lire les 100 dernières lignes
                lines = f.readlines()[-n:]
                intensities = []  # Liste pour stocker les intensités

                # Parcourir les lignes et extraire les intensités
                for i, line in enumerate(lines):
                    try:
                        line_data = json.loads(line.strip())  # Charger la ligne comme JSON
                        intensity = line_data.get("intensity", None)
                        if intensity is not None:
                            intensities.append(intensity)  # Ajouter l'intensité à la liste
                    except json.JSONDecodeError as e:
                        print(f"Erreur de décodage JSON à la ligne {i+1} pour le compteur {numero_serie}: {e}")

                # Ajouter les intensités au DataFrame des compteurs
                compteurs.at[idx, "intensities"] = intensities  # Assurez-vous que cela est bien mis à jour pour chaque ligne

                # Calculer la moyenne des intensités et l'ajouter comme une nouvelle colonne
                if intensities:
                    compteurs.at[idx, "moyenne_intensites"] = int(round(sum(intensities) / len(intensities)))
                else:
                    compteurs.at[idx, "moyenne_intensites"] = None  # Si aucune intensité, on met None

        except FileNotFoundError:
            print(f"Fichier manquant pour le compteur {numero_serie}")
        except KeyError:
            print(f"Données mal formées dans le fichier {numero_serie}")
        except Exception as e:
            print(f"Erreur inconnue pour le compteur {numero_serie}: {e}")

moyenne_i = int(round(compteurs["moyenne_intensites"].mean()))

# Charger le réseau de rues de Montpellier
montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="bike")

# Création de la figure et des axes
fig, ax = ox.plot_graph(montpellier_graph, show=False, close=False, node_size=0, edge_color="white", edge_linewidth=0.5, bgcolor="black")

# Fonction de mise à jour pour la vidéo 
def update(frame):
    ax.clear()  # Effacer l'ancienne image
    
    # Redessiner le réseau
    ox.plot_graph(montpellier_graph, ax=ax, show=False, close=False, node_size=0, edge_color="white", edge_linewidth=0.5, bgcolor="black")
    
    # Ajuster taille du compteur selon intensité 
    sizes = [((compteurs.iloc[i]['intensities'][frame]*50)/moyenne_i) if len(compteurs.iloc[i]['intensities']) > frame else 0 for i in range(len(compteurs))]
   
    # Afficher les compteurs avec des tailles de marqueurs variables
    # Afficher un halo (point plus large et moins transparent)
    compteurs.plot(ax=ax, marker='o', color='#9b4dca', markersize=[size+10 for size in sizes], alpha=0.3, label="Halo Compteurs", edgecolor='purple', linewidth=2)

    # Afficher le point principal (point violet plus petit et plus opaque)
    compteurs.plot(ax=ax, marker='o', color='#9b4dca', markersize=sizes, alpha=1, label="Compteurs", edgecolor='purple', linewidth=2)

    # Ajouter le titre et la légende
    ax.set_title(f"Frame: {frame}")

# Créer l'animation
ani = FuncAnimation(fig, update, frames=n, repeat=False)

# Création de l'instance writer avec les arguments nécessaires
writer = FFMpegWriter(fps=10, codec='libx264', bitrate=1800)

# Utilisation de writer lors de l'enregistrement
ani.save("compteurs_animation2.mp4", writer=writer)

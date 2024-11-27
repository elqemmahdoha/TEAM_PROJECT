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

# Initialiser les colonnes dans le GeoDataFrame
compteurs["intensities"] = None  # Pour stocker les intensités
compteurs["dates"] = None  # Pour stocker les dates correspondantes

# Extraction des intensités et des dates des n derniers jours 
n = 100
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
                dates = []  # Liste pour stocker les dates correspondantes

                # Parcourir les lignes et extraire les données nécessaires
                for i, line in enumerate(lines):
                    try:
                        line_data = json.loads(line.strip())  # Charger la ligne comme JSON
                        intensity = line_data.get("intensity", None)
                        date_observed = line_data.get("dateObserved", None)
                        
                        if intensity is not None:
                            intensities.append(intensity)  # Ajouter l'intensité à la liste
                        
                        if date_observed:
                            # Extraire uniquement la première partie de la plage de dates
                            date = date_observed.split("/")[0].split("T")[0]  # Garder seulement le début de la plage
                            dates.append(date)

                    except json.JSONDecodeError as e:
                        print(f"Erreur de décodage JSON à la ligne {i+1} pour le compteur {numero_serie}: {e}")

                # Ajouter les données au DataFrame des compteurs
                compteurs.at[idx, "intensities"] = intensities
                compteurs.at[idx, "dates"] = dates

                # Calculer la moyenne des intensités
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

# Déterminer la plage de dates pour l'animation (en supposant que les dates sont synchronisées)
# Les dates de la première colonne sont utilisées comme référence
common_dates = compteurs.iloc[0]["dates"]

# Calculer la moyenne des intensités globalement
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
    sizes = [
        ((compteurs.iloc[i]['intensities'][frame] * 70) / moyenne_i) 
        if len(compteurs.iloc[i]['intensities']) > frame else 0 
        for i in range(len(compteurs))
    ]
   
    # Afficher les compteurs avec des tailles de marqueurs variables
    # Afficher un halo (point plus large et moins transparent)
    compteurs.plot(ax=ax, marker='o', color='#9b4dca', markersize=[size+10 for size in sizes], alpha=0.3, label="Halo Compteurs", edgecolor='purple', linewidth=2)

    # Afficher le point principal (point violet plus petit et plus opaque)
    compteurs.plot(ax=ax, marker='o', color='#9b4dca', markersize=sizes, alpha=1, label="Compteurs", edgecolor='purple', linewidth=2)

    # Ajouter le titre avec la date correspondant à la frame
    current_date = common_dates[frame] if frame < len(common_dates) else "Date inconnue"
    ax.set_title(f"Date : {current_date}")

# Créer l'animation
ani = FuncAnimation(fig, update, frames=len(common_dates), repeat=False)

# Création de l'instance writer avec les arguments nécessaires
writer = FFMpegWriter(fps=10, codec='libx264', bitrate=1800)

# Utilisation de writer lors de l'enregistrement
ani.save("compteurs_animation.mp4", writer=writer)

import geopandas as gpd
import json
import osmnx as ox
import pandas as pd
import numpy as np  
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Chargement fichier courses Velomagg 
brut = pd.read_csv("data/video/courses/CoursesVelomagg_filtre.csv").dropna() 

# Chargement fichier GeoJSON contenant les points de comptage
compteurs = gpd.read_file("data/video/ecocompt/GeolocCompteurs.geojson")

# Date de la vidéo
date_video = pd.to_datetime("2024-10-07").date()

# Extraire les numéros de série des compteurs
compteurs["numero_serie"] = compteurs["N° Sér_1"].fillna(compteurs["N° Série"])

# Initialiser les colonnes dans le GeoDataFrame
compteurs["intensity"] = None  # Pour stocker les intensités
compteurs["date"] = None  # Pour stocker les dates correspondantes

for idx, row in compteurs.iterrows():
    numero_serie = row["numero_serie"]
    if pd.notnull(numero_serie):
        try:
            # Charger le fichier JSON correspondant
            filepath = f"data/video/ecocompt/filtered/MMM_EcoCompt_{numero_serie}_archive.json"
            with open(filepath, 'r', encoding='utf-8') as f:
                # Lire les 100 dernières lignes
                lines = f.readlines()
    
                # Parcourir les lignes et extraire les données nécessaires
                for i, line in enumerate(lines):
                    intensity = 0 
                    try:
                        line_data = json.loads(line.strip())  # Charger la ligne comme JSON
                        intensity_observed = line_data.get("intensity", None)
                        date_observed = line_data.get("dateObserved", None)
                        if date_observed:
                            # Extraire la date (avant "T")
                            date = pd.to_datetime(date_observed.split("/")[0].split("T")[0]).date()
                            if date == date_video:  # Filtrer uniquement pour date_video
                                if intensity_observed is not None:
                                    intensity = intensity_observed  # Ajouter l'intensité
                                    compteurs.at[idx, "intensity"] = intensity
                                    compteurs.at[idx, "date"] = date

                    except json.JSONDecodeError as e:
                        print(f"Erreur de décodage JSON à la ligne {i+1} pour le compteur {numero_serie}: {e}")

        except FileNotFoundError:
            print(f"Fichier manquant pour le compteur {numero_serie}")
        except KeyError:
            print(f"Données mal formées dans le fichier {numero_serie}")
        except Exception as e:
            print(f"Erreur inconnue pour le compteur {numero_serie}: {e}")

# Remplacer None par 0 dans 'intensity'
compteurs["intensity"] = compteurs["intensity"].fillna(0).astype(int)

# Remplacer None dans 'date' par date_video
compteurs["date"] = compteurs["date"].fillna(date_video)

# Transformer la colonne des départs en format date avec test d'erreur
try:
    brut['Departure'] = pd.to_datetime(brut['Departure'], errors='raise')
except ValueError as e:
    print("Erreur de conversion des dates :", e)
    # Optionnel : Trouver les valeurs problématiques
    invalid_dates = brut['Departure'][~brut['Departure'].str.match(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}')]
    print("Valeurs problématiques :", invalid_dates.tolist())

# Restreindre le fichier des courses à la date selectionnée 
courses = brut[brut['Departure'].dt.date == date_video].copy()

# Noms des stations (départ et arrivée) en supprimant les doublons 
stations = np.union1d(courses['Departure station'].unique(), courses['Return station'].unique())

# Coordonnées des stations 
with open("data/video/courses/PointsVelomagg.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Transformer le fichier JSON en dictionnaire coord_stations
coord_stations = {}
for feature in data['features']:
    nom = feature['properties']['nom']  # Nom de la station
    numero = feature['properties']['numero'] # Numéro de la station
    longitude, latitude = feature['geometry']['coordinates']  # Coordonnées [longitude, latitude]
    coord_stations[numero] = {'nom': nom, 'latitude': latitude, 'longitude': longitude}

# Rajouter les coordonnées au fichier
courses['latitude_depart'] = courses['Departure number'].map(lambda x: coord_stations.get(x, {}).get('latitude'))
courses['longitude_depart'] = courses['Departure number'].map(lambda x: coord_stations.get(x, {}).get('longitude'))
courses['latitude_retour'] = courses['Return number'].map(lambda x: coord_stations.get(x, {}).get('latitude'))
courses['longitude_retour'] = courses['Return number'].map(lambda x: coord_stations.get(x, {}).get('longitude'))

# Charger le réseau cycliste de Montpellier
montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="all")

# Création de la figure et des axes
fig, ax = ox.plot_graph(montpellier_graph, show=False, close=False, node_size=0, edge_color="white", edge_linewidth=0.5, bgcolor="black")

# Fonction de recherche du trajet le plus court entre deux stations 
def recherche_trajet(C):
    try:
        d_lat, d_lon = C['latitude_depart'], C['longitude_depart']   
        f_lat = C['latitude_retour'] 
        f_lon = C['longitude_retour']
        node_d = ox.distance.nearest_nodes(montpellier_graph, d_lon, d_lat)
        node_f = ox.distance.nearest_nodes(montpellier_graph, f_lon, f_lat)
        trajet = nx.shortest_path(montpellier_graph, node_d, node_f, weight="length")
        return trajet
    except Exception as e:
        print(f"Erreur  entre {C['Departure station']} et {C['Return station']}: {e}")
        return None
    
# Process des trajets 
trajets = [recherche_trajet(i) for _, i in courses.iterrows()]
#print(len(trajets))
#print(trajets)

# Initialisation des points et des lignes pour tous les trajets
def initialize_graph_objects(trajets, ax):
    points = []
    lignes = []
    
    # Paramètres de style pour les points et les lignes
    point_style = {'color': '#FFFFE0', 'marker': 'o'}
    line_style = {'color': '#FFFF00', 'linewidth': 1}
    
    for _ in trajets:
        # Créer un point et une ligne pour chaque trajet
        point, = ax.plot([], [], **point_style)  # La virgule est nécessaire pour déballer l'objet
        ligne, = ax.plot([], [], **line_style)
        
        points.append(point)
        lignes.append(ligne)
        
    return points, lignes

# Affectation par appel de la fonction
points, lignes = initialize_graph_objects(trajets, ax)

# Fonction d'initialisation de l'animation
def init():
    for point, ligne in zip(points, lignes):
        point.set_data([], [])
        ligne.set_data([], [])
    return points + lignes

def update(frame):
    # Trajets courses
    for i, trajet in enumerate(trajets):
        if frame < len(trajet):  # Afficher le trajet en cours
            x_vals = [montpellier_graph.nodes[node]['x'] for node in trajet[:frame + 1]]
            y_vals = [montpellier_graph.nodes[node]['y'] for node in trajet[:frame + 1]]
            lignes[i].set_data(x_vals, y_vals)
            points[i].set_data([montpellier_graph.nodes[trajet[frame]]['x']], [montpellier_graph.nodes[trajet[frame]]['y']])
        else:  # Cacher le trajet une fois terminé
            #lignes[i].set_data([], [])
            points[i].set_data([], [])
    # Compteurs
    compteurs.plot(ax=ax, marker='o', color='#9b4dca', markersize=[100 for i in range(len(compteurs))], alpha=1, label="Compteurs", edgecolor='purple', linewidth=2)
    
    return points + lignes
    
# Calculer le nombre total de frames basé sur le plus long trajet
frames = max(len(trajet) for trajet in trajets)

# Ajout de la date 
ax.set_title(f"Date : {date_video}")

# Créer l'animation
ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, repeat=False)

# Création de l'instance writer avec les arguments nécessaires
writer = FFMpegWriter(fps=10, codec='libx264', bitrate=1800)

# Sauvegarder l'animation sous forme de fichier MP4
ani.save("docs/bicycle.mp4", writer=writer)
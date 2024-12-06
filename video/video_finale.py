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

# Date de la vidéo
date_video = pd.to_datetime("2024-10-07").date()

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
        print(C)
        d_lat, d_lon = C['latitude_depart'], C['longitude_depart']  
        print(d_lat)
        print(d_lon) 
        f_lat = C['latitude_retour'] 
        f_lon = C['longitude_retour']
        node_d = ox.distance.nearest_nodes(montpellier_graph, d_lon, d_lat)
        node_f = ox.distance.nearest_nodes(montpellier_graph, f_lon, f_lat)
        print(node_d)
        print(node_f)
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
    point_style = {'color': 'cyan', 'marker': 'o'}
    line_style = {'color': 'white', 'linewidth': 1}
    
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
    for i, trajet in enumerate(trajets):
        if frame < len(trajet):  # Afficher le trajet en cours
            x_vals = [montpellier_graph.nodes[node]['x'] for node in trajet[:frame + 1]]
            y_vals = [montpellier_graph.nodes[node]['y'] for node in trajet[:frame + 1]]
            lignes[i].set_data(x_vals, y_vals)
            points[i].set_data([montpellier_graph.nodes[trajet[frame]]['x']], [montpellier_graph.nodes[trajet[frame]]['y']])
        else:  # Cacher le trajet une fois terminé
            lignes[i].set_data([], [])
            points[i].set_data([], [])
    return points + lignes

# Calculer le nombre total de frames basé sur le plus long trajet
max_frames = max(len(trajet) for trajet in trajets)
print(max_frames)

# Créer l'animation
ani = FuncAnimation(fig, update, frames=max_frames, init_func=init, blit=True, repeat=False)

# Création de l'instance writer avec les arguments nécessaires
writer = FFMpegWriter(fps=10, codec='libx264', bitrate=1800)

# Sauvegarder l'animation sous forme de fichier MP4
ani.save("test.mp4", writer=writer)
from .data_loader import load_courses, load_compteurs, load_coord_stations, update_intensity_for_compteurs
from .trajets import load_montpellier_graph, find_shortest_path
from .animation import TrajetAnimation
import osmnx as ox
import time

def main():
    """
    Script principal pour l'analyse et la visualisation des trajets de vélos à Montpellier.

    Ce script charge les données nécessaires pour l'analyse des trajets de vélos, effectue des mises à jour sur les compteurs, calcule les trajets les plus courts entre les stations de départ et de retour, et génère une animation des trajets sur un fond de carte de la ville.

    Le processus inclut les étapes suivantes :
    1. Chargement des données : 
    - Les informations sur les courses de vélos depuis un fichier CSV.
    - Les informations géospatiales des compteurs à partir d'un fichier GeoJSON.
    - Les coordonnées des stations depuis un fichier JSON.
    
    2. Mise à jour des intensités des compteurs en fonction de la date vidéo spécifiée.

    3. Calcul des coordonnées de départ et de retour pour chaque course et ajout à un DataFrame.

    4. Calcul du trajet le plus court entre les stations de départ et de retour en utilisant un graphe du réseau cycliste de Montpellier.

    5. Création d'une animation des trajets avec les données géographiques et les informations des compteurs.

    6. Sauvegarde de l'animation générée sous forme de fichier vidéo au format MP4.

    Modules utilisés :
    - `data_loader`: Pour charger les données nécessaires à l'analyse.
    - `trajets`: Pour calculer les trajets les plus courts.
    - `animation`: Pour générer et enregistrer l'animation des trajets.
    - `osmnx`: Pour manipuler les graphes du réseau cycliste de Montpellier.

    Temps d'exécution : entre 3 et 4 minutes.

    """

    # Chargement des données
    date_video = "2024-10-07"
    courses = load_courses("data/video/courses/CoursesVelomagg_filtre.csv", date_video)
    compteurs = load_compteurs("data/video/ecocompt/GeolocCompteurs.geojson")
    coord_stations = load_coord_stations("data/video/courses/PointsVelomagg.json")

    # Mise à jour des intensités des compteurs
    compteurs = update_intensity_for_compteurs(compteurs, date_video)

    # Mise à jour du dataframe courses
    courses['latitude_depart'] = courses['Departure number'].map(lambda x: coord_stations.get(x, {}).get('latitude'))
    courses['longitude_depart'] = courses['Departure number'].map(lambda x: coord_stations.get(x, {}).get('longitude'))
    courses['latitude_retour'] = courses['Return number'].map(lambda x: coord_stations.get(x, {}).get('latitude'))
    courses['longitude_retour'] = courses['Return number'].map(lambda x: coord_stations.get(x, {}).get('longitude'))

    # Préparer les trajets
    trajets = []
    montpellier_graph = load_montpellier_graph()
    for _, row in courses.iterrows():
        start_coords = (row['latitude_depart'], row['longitude_depart'])
        end_coords = (row['latitude_retour'], row['longitude_retour'])
        trajet = find_shortest_path(montpellier_graph, start_coords, end_coords)
        trajets.append(trajet)

    # Créer l'animation
    fig, ax = ox.plot_graph(montpellier_graph, show=False, close=False, node_size=0, edge_color="white", edge_linewidth=0.5, bgcolor="black")
    anim_bicycle = TrajetAnimation(trajets, montpellier_graph, compteurs, ax, fig, date_video)
    anim_bicycle.create_animation("docs/bicycle.mp4", fps=10, bitrate=1800)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Temps : {end - start:.5f} s")
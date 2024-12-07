from .data_loader import load_courses, load_compteurs, load_coord_stations, update_intensity_for_compteurs
from .trajets import load_montpellier_graph, find_shortest_path
from .animation import TrajetAnimation
import osmnx as ox
import time

def main():
    # Chargement des données
    date_video = "2024-10-07"
    courses = load_courses("data/video/courses/CoursesVelomagg_filtre.csv", date_video)
    compteurs = load_compteurs("data/video/ecocompt/GeolocCompteurs.geojson")
    coord_stations = load_coord_stations("data/video/courses/PointsVelomagg.json")

    # Mise à jour des intensités des compteurs
    compteurs = update_intensity_for_compteurs(compteurs, date_video)
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
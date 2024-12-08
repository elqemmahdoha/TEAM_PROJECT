import osmnx as ox
import networkx as nx

def load_montpellier_graph() -> nx.MultiDiGraph:
    """
    Charge le réseau cycliste de Montpellier en utilisant OSMnx.

    Retourne :
        nx.MultiDiGraph : Le graphe routier de Montpellier avec toutes les informations de nœuds et d'arêtes.
    """
    montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="all")
    return montpellier_graph

def find_shortest_path(montpellier_graph: nx.MultiDiGraph, start_coords: tuple, end_coords: tuple) -> list:
    """
    Trouve le trajet le plus court entre deux points dans un graphe en fonction de leurs coordonnées.

    Arguments :
        montpellier_graph (nx.MultiDiGraph) : Le graphe routier chargé de Montpellier.
        start_coords (tuple) : Coordonnées de départ sous la forme (latitude, longitude).
        end_coords (tuple) : Coordonnées d'arrivée sous la forme (latitude, longitude).

    Retourne :
        list : Une liste des nœuds représentant le chemin le plus court entre les deux points.
    """
    d_lat, d_lon = start_coords
    f_lat, f_lon = end_coords

    # Trouver les nœuds les plus proches des coordonnées de départ et d'arrivée
    node_d = ox.distance.nearest_nodes(montpellier_graph, d_lon, d_lat)
    node_f = ox.distance.nearest_nodes(montpellier_graph, f_lon, f_lat)

    # Calculer le chemin le plus court basé sur la longueur des arêtes
    trajet = nx.shortest_path(montpellier_graph, node_d, node_f, weight="length")
    return trajet

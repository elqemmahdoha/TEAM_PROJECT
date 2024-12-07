import osmnx as ox
import networkx as nx

def load_montpellier_graph():
    """Charge le réseau cycliste de Montpellier."""
    montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="all")
    return montpellier_graph

def find_shortest_path(montpellier_graph, start_coords, end_coords):
    """Trouve le trajet le plus court entre deux points."""
    d_lat, d_lon = start_coords
    f_lat, f_lon = end_coords
    node_d = ox.distance.nearest_nodes(montpellier_graph, d_lon, d_lat)
    node_f = ox.distance.nearest_nodes(montpellier_graph, f_lon, f_lat)
    trajet = nx.shortest_path(montpellier_graph, node_d, node_f, weight="length")
    return trajet
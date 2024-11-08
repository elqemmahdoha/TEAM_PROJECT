#%%
import pandas as pd
import geopandas as gpd
import osmnx as ox  
import matplotlib.pyplot as plt

# Charger le réseau de rues de Montpellier
montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="bike")

# Charger le fichier GeoJSON contenant les points de comptage
compteurs = gpd.read_file("data\ecocompt\MMM_MMM_GeolocCompteurs.geojson")

# Création figure
fig, ax = ox.plot_graph(montpellier_graph, show=False, close=False, node_size=0, edge_color="black", edge_linewidth=0.5, bgcolor="white")

# Afficher les points de comptage par-dessus le réseau
compteurs.plot(ax=ax, marker='o', color='red', markersize=20, label="Compteurs")

# Affiche la figure
plt.show()
import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Charger le réseau de rues de Montpellier
montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="bike")

# Charger le fichier GeoJSON contenant les points de comptage
compteurs = gpd.read_file("data/ecocompt/GeolocCompteurs.geojson")

# Création de la figure et des axes
fig, ax = ox.plot_graph(montpellier_graph, show=False, close=False, node_size=0, edge_color="black", edge_linewidth=0.5, bgcolor="white")

# Fonction de mise à jour pour l'animation
def update(frame):
    ax.clear()  # Effacer l'ancienne image
    
    # Redessiner le réseau
    ox.plot_graph(montpellier_graph, ax=ax, show=False, close=False, node_size=0, edge_color="black", edge_linewidth=0.5, bgcolor="white")
    
    # Créer une taille aléatoire pour chaque compteur
    sizes = [random.randint(10, 100) for _ in range(len(compteurs))]
    
    # Afficher les compteurs avec des tailles de marqueurs variables
    compteurs.plot(ax=ax, marker='o', color='red', markersize=sizes, label="Compteurs")
    
    # Ajouter le titre et la légende
    ax.set_title(f"Frame: {frame}")
    plt.legend()

# Créer l'animation
ani = FuncAnimation(fig, update, frames=100, repeat=False)

# Sauvegarder la vidéo
ani.save("compteurs_animation.gif", writer="Pillow", fps=10)
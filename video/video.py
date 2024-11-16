import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import pandas as pd
import json
import os

# Charger le fichier GeoJSON contenant les points de comptage
compteurs = gpd.read_file("data/video/ecocompt/GeolocCompteurs.geojson")

# Extraire les numéros de série des compteurs
compteurs["numero_serie"] = compteurs["N° Sér_1"].fillna(compteurs["N° Série"])

for _, row in compteurs.iterrows():
    numero_serie = row["numero_serie"]
    #print(numero_serie)
    if pd.notnull(numero_serie):
        try:
            # Charger le fichier JSON correspondant
            filepath = f"data/video/ecocompt/MMM_EcoCompt_{numero_serie}_archive.json"
            with open(filepath, 'r') as f:
                # Lire les 100 dernières lignes
                lines = f.readlines()[-100:]
                comptages = []

                # Afficher la première ligne du fichier JSON chargé
                #print("Première ligne du fichier JSON:")
                first_line = lines[0].strip()  # Enlever les espaces superflus
                #print(first_line)  # Utilisation de strip() pour enlever les espaces superflus

                # Charger la ligne JSON en tant que dictionnaire Python
                first_line_data = json.loads(first_line)

                # Extraire et afficher l'intensité
                intensity = first_line_data.get("intensity", None)  # Utiliser get pour éviter une erreur si la clé manque
                #print(f"Intensité extraite: {intensity}")

        except FileNotFoundError:
            print(f"Fichier manquant pour le compteur {numero_serie}")
        except KeyError:
            print(f"Données mal formées dans le fichier {numero_serie}")
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON pour le compteur {numero_serie}: {e}")
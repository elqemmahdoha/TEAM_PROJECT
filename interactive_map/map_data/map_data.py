import pandas as pd
import json
pd.options.mode.chained_assignment = None
# Importation des données des compteurs triées
def load_map_interactive_data():
    """
    Charge les données des compteurs triées pour l'analyse interactive de la carte.

    Le processus de chargement des données comprend les étapes suivantes :
    1. Charge les données des compteurs à partir d'un fichier CSV contenant une semaine précise classique.
    2. Réorganise les données pour les regrouper par jour, latitude, et longitude.
    3. Supprime les valeurs manquantes.
    4. Supprime les compteurs trop éloignés.
    5. Calcule la moyenne de l'intensité pour chaque groupe de données.

    Returns:
        pd.DataFrame: Un DataFrame contenant les données des compteurs triées.
    """
    weeklyd = pd.read_csv("data/donnees_hebdo.csv", sep=";", na_values="Null", low_memory=False)
    weeklyd = pd.melt(weeklyd, id_vars=["N° Série", "Latitude", "Longitude"], 
                     value_vars=["18/3", "19/3", "20/3", "21/3", "22/3", "23/3", "24/3"],
                     var_name="Jour", value_name="Intensité")
    weeklyd = weeklyd.dropna()
    compteurs_todrop = weeklyd[(weeklyd["N° Série"] == "X2H22104765") | 
                               (weeklyd["N° Série"] == "X2H21070350")].index
    weeklyd.drop(compteurs_todrop, inplace=True) # Suppression des compteurs trop éloignés
    weeklyd = weeklyd.groupby(["Jour", "Latitude", "Longitude"])["Intensité"].mean().reset_index(name="Intensité")
    return weeklyd

def load_coord_stations(file_path):
    """
    Charge les coordonnées des stations Velomagg à partir d'un fichier JSON.
    
    Args:
    - file_path (str): Chemin du fichier JSON contenant les coordonnées des stations Velomagg.
    
    Returns:
    - dict: Dictionnaire contenant les coordonnées des stations Velomagg.
    """
    with open(file_path) as f:
        velomagg_geoloc = json.load(f)
    
    coord_stations = {}
    for feature in velomagg_geoloc["features"]:
        station_id = feature["properties"]["number"]
        station_name = feature["properties"]["name"]
        station_lat = feature["geometry"]["coordinates"][1]
        station_lon = feature["geometry"]["coordinates"][0]
        coord_stations[station_id] = {
            "name": station_name,
            "latitude": station_lat,
            "longitude": station_lon
        }
    
    return coord_stations
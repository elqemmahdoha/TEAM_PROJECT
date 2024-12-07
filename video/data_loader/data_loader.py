import geopandas as gpd
import pandas as pd
import json

def load_courses(file_path: str, date_video: str) -> pd.DataFrame:
    brut = pd.read_csv(file_path).dropna()
    brut['Departure'] = pd.to_datetime(brut['Departure'], errors='raise')
    courses = brut[brut['Departure'].dt.date == pd.to_datetime(date_video).date()].copy()
    return courses

def load_compteurs(file_path: str) -> gpd.GeoDataFrame:
    compteurs = gpd.read_file(file_path)
    compteurs["numero_serie"] = compteurs["N° Sér_1"].fillna(compteurs["N° Série"])
    compteurs["intensity"] = None
    compteurs["date"] = None
    return compteurs

def load_coord_stations(json_path: str) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    coord_stations = {}
    for feature in data['features']:
        nom = feature['properties']['nom']
        numero = feature['properties']['numero']
        longitude, latitude = feature['geometry']['coordinates']
        coord_stations[numero] = {'nom': nom, 'latitude': latitude, 'longitude': longitude}
    
    return coord_stations

def update_intensity_for_compteurs(compteurs: gpd.GeoDataFrame, date_video) -> gpd.GeoDataFrame:
    """
    Met à jour les intensités et les dates des compteurs à partir des fichiers JSON spécifiques.
    """
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
                                if date == pd.to_datetime(date_video).date():  # Filtrer uniquement pour date_video
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
    
    return compteurs

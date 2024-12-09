import geopandas as gpd
import json
import pandas as pd
from collections import defaultdict

def charger_compteurs(filepath):
    """
    Charge un fichier GeoJSON contenant des données sur les compteurs et extrait les numéros de série des compteurs.

    Arguments :
        filepath : Le chemin vers le fichier GeoJSON contenant les données des compteurs.

    Retourne :
        compteurs : Un GeoDataFrame avec les données des compteurs, incluant une nouvelle colonne 'numero_serie'
                            extraite des colonnes 'N° Sér_1' et 'N° Série'.
    """
    compteurs = gpd.read_file(filepath)
    compteurs["numero_serie"] = compteurs["N° Sér_1"].fillna(compteurs["N° Série"])
    return compteurs

def charger_intensites_par_mois(compteurs, date_debut, date_fin):
    """
    Extrait les intensités des compteurs pour une période donnée et calcule la moyenne mensuelle des intensités,
    puis stocke ces moyennes dans les colonnes appropriées.

    Arguments :
        compteurs : Le GeoDataFrame des compteurs contenant une colonne 'numero_serie'.
        date_debut : La date de début de la période d'analyse.
        date_fin : La date de fin de la période d'analyse.

    Retourne :
        compteurs : Le GeoDataFrame mis à jour avec des colonnes pour chaque mois ('mean_01', 'mean_02', etc.)
                            représentant les moyennes mensuelles des intensités pour chaque compteur.
    """
    mois_colonnes_moyenne = [f"mean_{str(mois).zfill(2)}" for mois in range(3, 11)]
    for col in mois_colonnes_moyenne:
        compteurs[col] = None

    for idx, row in compteurs.iterrows():
        numero_serie = row["numero_serie"]
        if pd.notnull(numero_serie):
            try:
                filepath = f"data/files/filtered/MMM_EcoCompt_{numero_serie}_archive.json"
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    intensities_by_month = defaultdict(list)

                    for i, line in enumerate(lines):
                        try:
                            line_data = json.loads(line.strip())
                            intensity = line_data.get("intensity", None)
                            date_observed = line_data.get("dateObserved", None)

                            if date_observed:
                                date = pd.to_datetime(date_observed.split("/")[0].split("T")[0]).date()
                                if date_debut <= date <= date_fin:
                                    month = date.strftime('%m')
                                    if intensity is not None:
                                        intensities_by_month[month].append(intensity)

                        except json.JSONDecodeError as e:
                            print(f"Erreur de décodage JSON à la ligne {i+1} pour le compteur {numero_serie}: {e}")

                    for month, intensities in intensities_by_month.items():
                        if intensities:
                            mean_column = f"mean_{month}"
                            compteurs.loc[idx, mean_column] = sum(intensities) / len(intensities)

            except FileNotFoundError:
                print(f"Fichier manquant pour le compteur {numero_serie}")
            except Exception as e:
                print(f"Erreur inconnue pour le compteur {numero_serie}: {e}")
    
    return compteurs

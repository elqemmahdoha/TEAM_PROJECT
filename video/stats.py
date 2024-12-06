import geopandas as gpd
import json
from collections import defaultdict
import pandas as pd
import os
import plotly.express as px
import seaborn as sns 
import matplotlib.pyplot as plt

# Créer un sous-répertoire de destination pour les figures
dossier_destination = "docs\\figures"
os.makedirs(dossier_destination, exist_ok=True)  # Crée le dossier s'il n'existe pas

# Chemins 
chemin_average_intensity = os.path.join(dossier_destination, "average_intensity_month.html")

# Charger le fichier GeoJSON contenant les points de comptage
compteurs = gpd.read_file("data/video/ecocompt/GeolocCompteurs.geojson")

# Extraire les numéros de série des compteurs
compteurs["numero_serie"] = compteurs["N° Sér_1"].fillna(compteurs["N° Série"])

date_debut = pd.to_datetime("2024-03-01").date()
date_fin = pd.to_datetime("2024-10-31").date()

# Colonnes pour les moyennes des intensités mensuelles
mois_colonnes_moyenne = [f"mean_{str(mois).zfill(2)}" for mois in range(3, 11)]

# Initialiser les colonnes pour les moyennes mensuelles
for col in mois_colonnes_moyenne:
    compteurs[col] = None

# Parcourir les compteurs pour extraire les données
for idx, row in compteurs.iterrows():
    numero_serie = row["numero_serie"]
    if pd.notnull(numero_serie):
        try:
            # Charger le fichier JSON correspondant
            filepath = f"data/video/ecocompt/filtered/MMM_EcoCompt_{numero_serie}_archive.json"
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()  # Lire toutes les lignes
                intensities_by_month = defaultdict(list)  # Dictionnaire pour stocker les intensités par mois

                for i, line in enumerate(lines):
                    try:
                        line_data = json.loads(line.strip())  # Charger la ligne comme JSON
                        intensity = line_data.get("intensity", None)
                        date_observed = line_data.get("dateObserved", None)

                        if date_observed:
                            # Extraire uniquement la première partie de la plage de dates
                            date = pd.to_datetime(date_observed.split("/")[0].split("T")[0]).date()

                            # Filtrer par la plage de dates
                            if date_debut <= date <= date_fin:
                                month = date.strftime('%m')  # Extraire le mois au format 'MM'
                                if intensity is not None:
                                    intensities_by_month[month].append(intensity)

                    except json.JSONDecodeError as e:
                        print(f"Erreur de décodage JSON à la ligne {i+1} pour le compteur {numero_serie}: {e}")

                # Calculer les moyennes mensuelles et les ajouter aux colonnes correspondantes
                for month, intensities in intensities_by_month.items():
                    if intensities:  # Si des intensités existent pour ce mois
                        mean_column = f"mean_{month}"
                        compteurs.loc[idx, mean_column] = sum(intensities) / len(intensities)

        except FileNotFoundError:
            print(f"Fichier manquant pour le compteur {numero_serie}")
        except Exception as e:
            print(f"Erreur inconnue pour le compteur {numero_serie}: {e}")

# Gestion pb Gerhardt 
# Identifier la ligne correspondant à "Compteur Vélo Gerhardt"
ligne_gerhardt = compteurs["Nom du com"] == "Compteur Vélo Gerhardt"

# Mettre toutes les colonnes des moyennes d'intensités à None pour cette ligne
mois_colonnes_moyenne = [col for col in compteurs.columns if col.startswith("mean_")]
compteurs.loc[ligne_gerhardt, mois_colonnes_moyenne] = None

# Créer un dictionnaire pour mapper les colonnes à des noms de mois
month_mapping = {
    "mean_03": "Mars",
    "mean_04": "Avril",
    "mean_05": "Mai",
    "mean_06": "Juin",
    "mean_07": "Juillet",
    "mean_08": "Août",
    "mean_09": "Septembre",
    "mean_10": "Octobre"
}

# Sélectionner les colonnes qui contiennent "mean_" dans leur nom
mean_columns = [col for col in compteurs.columns if col.startswith("mean_")]

# Calculer la moyenne de chaque colonne en ignorant les NaN
mean_values = compteurs[mean_columns].apply(pd.to_numeric, errors='coerce').mean() # numeric pour ne pas traiter les None -> Nan 

# Créer un nouveau DataFrame pour afficher les moyennes avec noms de mois
tableau_moyennes = pd.DataFrame({
    "Month": [month_mapping[col] for col in mean_columns],  # Utiliser les noms de mois
    "Average Intensity": mean_values.values                # Valeurs des moyennes
})

# Créer le graphique avec Plotly
fig = px.line(tableau_moyennes, x='Month', y='Average Intensity', 
              markers=True, title="Passage moyen devant les éco-compteurs par mois sur l'année 2024")

# Personnaliser la couleur de la ligne et des axes
fig.update_traces(line=dict(color='darkviolet'))  # Couleur de la ligne en violet foncé

# Personnaliser les axes et le fond
fig.update_layout(
    xaxis_title="Mois",
    yaxis_title="Intensité de passage moyenne",
    template="plotly_white",  # Style léger avec fond blanc
    showlegend=True
)

# Enregistrement de la figure 
fig.write_html(chemin_average_intensity)

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
# Importation des données des courses Velomagg
rd_velomagg = pd.read_csv("data/video/courses/TAM_MMM_CoursesVelomagg.csv", encoding="utf-8-sig")

# Correction de l'encodage des caractères pour faire disparaître les caractères spéciaux
def correct_encoding(value):
    if isinstance(value, str):
        return value.encode("latin1", errors="replace").decode("utf-8", errors="replace")
    return value

rd_velomagg = rd_velomagg.apply(lambda col: col.apply(correct_encoding) if col.dtype == "object" else col)

rd_velomagg["Date"] = pd.to_datetime(rd_velomagg["Departure"]).dt.date
# Choix des dates de la semaine à visualiser (mêmes dates que celles des données des compteurs)
date_debut = pd.to_datetime("2024-03-18").date()
date_fin = pd.to_datetime("2024-03-24").date()

rd_velomagg = rd_velomagg[(rd_velomagg["Date"] >= date_debut) & (rd_velomagg["Date"] <= date_fin)]
dates = pd.date_range(date_debut, date_fin).date # Création de la liste des dates de la semaine
weekdays = {date.strftime("%A"): date for date in dates} # Création d'un dictionnaire pour associer les jours de la semaine aux dates en français
# Création d'un graphique interactif pour visualiser les retraits et dépôts des Vélomaggs
def plot_interactive_graph(selected_day="lundi", show="both"):
    fig = make_subplots(rows=1, cols=1) # Création d'une figure avec un seul subplot

    for idx, (jour, date) in enumerate(weekdays.items()):
        rd_velo_par_jour = rd_velomagg[rd_velomagg["Date"] == date] # Filtrage des données par date
        
        r_sum = rd_velo_par_jour["Departure station"].value_counts() # Comptage des retraits par station
        d_sum = rd_velo_par_jour["Return station"].value_counts() # Comptage des dépôts par station

        stations = sorted(set(r_sum.index).union(set(d_sum.index))) # Création de la liste des stations
        r_sum = r_sum.reindex(stations, fill_value=0)
        d_sum = d_sum.reindex(stations, fill_value=0)
        # Ajout des barres pour les retraits
        fig.add_trace(go.Bar(
            y=r_sum, 
            x=stations, 
            name=f"Retrait - {jour}", 
            marker=dict(color="plum"),
            visible=(jour.lower() == selected_day.lower()) # Affichage du jour sélectionné, par défaut lundi
        ))
        # Ajout des barres pour les dépôts
        fig.add_trace(go.Bar(
            y=d_sum, 
            x=stations, 
            name=f"Dépôt - {jour}", 
            marker=dict(color="magenta"),
            visible=(jour.lower() == selected_day.lower())
        ))

    fig.update_layout( # Mise en beauté du graphique
        title="Retraits et Dépôts des Vélomaggs", 
        yaxis_title="Nombre de retraits ou dépôts",
        xaxis_title="Stations",
        barmode='group', # Affichage des barres groupées/côte à côte
        xaxis=dict(
            tickangle=-45, # Rotation des étiquettes de l'axe des abscisses
            showgrid=True,    
            gridcolor='LightGrey', 
            gridwidth=1,    
        ),
        yaxis=dict(
            showgrid=True,   
            gridcolor='LightGrey',
            gridwidth=1,  
        ), 
        legend=dict( # Positionnement de la légende
            yanchor="bottom",
            y=0,
            xanchor="left",
            x=1,
        ),
        bargap=0.05,   # Espacement entre les barres
        autosize=False,  # Ajustement manuel pour correspondre aux dimensions du site
        width=1300,
        height=1200,   
        template="simple_white",
        # Ajout d'un menu déroulant pour sélectionner un jour de la semaine
        updatemenus=[
            {
            "buttons": [
                {
                    "args": ["visible", [False] * len(weekdays) * 2],  
                    "label": "Sélectionner un jour",
                    "method": "restyle"
                },
                *[
                    {
                        "args": [
                            "visible", 
                            [i // 2 == idx for i in range(len(weekdays) * 2)]
                        ],
                        "label": jour,
                        "method": "restyle"
                    }
                    for idx, jour in enumerate(weekdays)
                ],
            ],
            "direction": "down",
            "showactive": True,
            "x": 1,
            "xanchor": "left",
            }
        ],
    )

    fig.write_html("docs/graphique_interactif.html") # Sauvegarde du graphique interactif

plot_interactive_graph(selected_day="lundi", show="both")

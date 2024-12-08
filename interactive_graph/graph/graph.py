import plotly.graph_objects as go
from graph_data import load_graph_data
from plotly.subplots import make_subplots
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Création d'un graphique interactif pour visualiser les retraits et dépôts des Vélomaggs
def plot_interactive_graph(selected_day="lundi", show="both"):
    """
    Création d'un graphique interactif pour visualiser les retraits et dépôts des Vélomaggs.
    
    Parameters
    ----------
    selected_day : str
        Jour de la semaine à afficher
        show : str
        
    Returns
    -------
    go.Figure
        Graphique interactif des retraits et dépôts des Vélomaggs
    """
    rd_velomagg, weekdays = load_graph_data() # Chargement des données pour les graphiques interactifs
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
    return fig

import time 
start = time.time()
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
import branca.colormap as cm

pd.options.mode.chained_assignment = None

sf = gpd.read_file("/Users/lauracletz/HAX712X/TEAM_PROJECT/data/ecocompt/MMM_MMM_GeolocCompteurs.geojson")

#On retire les deux compteurs qui sont trop loin de Montpellier Métropôle
compteurs_todrop = sf[
    (sf["N° Série"] == "X2H22104765")
    & (sf["N° Série"] == "X2H21070350")
].index
sf.drop(compteurs_todrop, inplace=True)


centre = [43.62505, 3.862038]
Montpellier = folium.Map(location=centre, zoom_start=6.5, tiles=None)
folium.GeoJson(
    sf[["geometry"]],
    zoom_on_click=True,
    style_function=lambda feature: {
        "fillColor": "#003322",
        "color": "grey",
        "weight": 2,
        "dashArray": "5, 5",
        "fillOpacity": 0.01,
    }
).add_to(Montpellier)


color_mapa = cm.LinearColormap(
    colors=["red", "orange", "yellow"],
    caption="Densité du trafic cycliste",
)
svg_style = "<style>svg#legend {background-color: rgba(255,255,255,0.5);}</style>"

Montpellier.get_root().header.add_child(folium.Element(svg_style))
color_mapa.add_to(Montpellier)
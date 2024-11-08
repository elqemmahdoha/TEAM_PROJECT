import geopandas as gpd
import pandas as pd
import folium
import json
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
import branca.colormap as cm
pd.options.mode.chained_assignment = None


sf = gpd.read_file("data/openstreetdata/contour-du-departement.geojson")
centre = [43.62505, 3.862038]
Montpellier = folium.Map(location=centre, zoom_start=10.5, tiles="OpenStreetMap")


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


weeklyd = pd.read_csv("data/donnees_hebdo.csv", sep=";", na_values="Null", low_memory=False)
weeklyd = pd.melt(weeklyd, id_vars=["N° Série", "Latitude", "Longitude"], 
                 value_vars=["18/3", "19/3", "20/3", "21/3", "22/3", "23/3", "24/3"],
                 var_name="Jour", value_name="Intensité")
weeklyd = weeklyd.dropna()
compteurs_todrop = weeklyd[(weeklyd["N° Série"] == "X2H22104765") | 
                           (weeklyd["N° Série"] == "X2H21070350")].index
weeklyd.drop(compteurs_todrop, inplace=True)
weeklyd = weeklyd.groupby(["Jour", "Latitude", "Longitude"])["Intensité"].mean().reset_index(name="Intensité")


grad = {0: "#ffff00", 0.5: "#ffcc66", 0.8: "#aa00aa", 1: "#800080"}
color_mapa = cm.LinearColormap(
    colors=list(grad.values()),  
    vmin=0, vmax=weeklyd["Intensité"].max(), 
    caption="Prédiction du trafic cycliste à Montpellier",
)
svg_style = "<style>svg#legend {background-color: rgba(255,255,255,0.5);}</style>"
Montpellier.get_root().header.add_child(folium.Element(svg_style))
color_mapa.add_to(Montpellier)

days = ["18/3", "19/3", "20/3", "21/3", "22/3", "23/3", "24/3"]
day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

day_feature_groups = []
for day, day_name in zip(days, day_names):
    data = weeklyd[weeklyd["Jour"] == day]
    data["Intensité"] *= 10
    heat_data = data[["Latitude", "Longitude", "Intensité"]].values.tolist()
    feature_group = folium.FeatureGroup(name=day_name, show=True)
    heat_map = HeatMap(
        heat_data,
        gradient=grad,
        radius=30,  
        blur=15,    
    )
    feature_group.add_child(heat_map)
    Montpellier.add_child(feature_group)
    
    day_feature_groups.append(feature_group)


'''
velo_orange = images/logo_velo_orange.png
icon = folium.CustomIcon(
    velo_orange,
    icon_size=(2, 2),
    icon_anchor=(2, 2),
    popup_anchor=(2, 2)
)

with open('data/openstreetdata/MMM_MMM_Velomagg.json',) as f:
    velomagg_geoloc = json.load(f)

for i in velomagg_geoloc["features"]:
    folium.Marker(location=velomagg_geoloc[[["coordinates"]]], 
            icon=velo_orange, 
            popup=velomagg_geoloc[[["nom"]]]).add_to(Montpellier)
'''

folium.LayerControl(position="topleft", collapsed=True, opacity=0.7).add_to(Montpellier)
GroupedLayerControl(
    position="topleft",
    groups={"Jours de la semaine": day_feature_groups},
    collapsed=False,
).add_to(Montpellier)

#Montpellier

#TO_REMOVE
Montpellier.save("mtp_interactive_test.html")

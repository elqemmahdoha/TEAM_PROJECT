import time
start = time.time()
import pandas as pd
import folium
import json
from folium.plugins import HeatMap, GroupedLayerControl
import branca.colormap as cm
pd.options.mode.chained_assignment = None


Montpellier = folium.Map(location=[43.62505, 3.862038], zoom_start=10.5, tiles=None)


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


with open('data/openstreetdata/MMM_MMM_Velomagg.json') as f:
    velomagg_geoloc = json.load(f)

for feature in velomagg_geoloc["features"]:
    lon, lat = feature["geometry"]["coordinates"]
    name = feature["properties"].get("nom", "Station Velomagg")

    folium.Marker(
        location=[lat, lon], 
        icon=folium.Icon(icon="bicycle", 
                    prefix="fa", icon_color="black", 
                    color="black", icon_size=(10, 10), 
                    shadow_size=(0,0)), 
        popup=folium.Popup(name, parse_html=True), 
    ).add_to(Montpellier)


GroupedLayerControl(
    position="topleft",
    groups={"Jours de la semaine": day_feature_groups},
    collapsed=False,
).add_to(Montpellier)

folium.TileLayer("OpenStreetMap", name="Street Map").add_to(Montpellier)
folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Satellite',
        overlay = False,
        control = True).add_to(Montpellier)
folium.LayerControl(position="topleft", collapsed=False, opacity=0.7).add_to(Montpellier)



Montpellier.save("mtp_interactive.html")
end = time.time()
print(f"Temps : {end - start:.5f} s")
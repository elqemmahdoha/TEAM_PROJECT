import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
import branca.colormap as cm

pd.options.mode.chained_assignment = None

sf = gpd.read_file("data/openstreetdata/contour-du-departement.geojson")
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
    caption="Prédiction du trafic cycliste à Montpellier",
)
svg_style = "<style>svg#legend {background-color: rgba(255,255,255,0.5);}</style>"

Montpellier.get_root().header.add_child(folium.Element(svg_style))
color_mapa.add_to(Montpellier)

grad = {0: "#0d0887", 0.1: "#0d0887", 0.2: "#0d0887", 0.3: "#0d0887", 0.4: "#0d0887", 0.5: "#6a00a8", 0.6: "#b12a90", 0.7: "#e16462", 0.8: "#fca636", 0.9: "#fcce25", 1: "#f0f921"}

weeklyd = pd.read_csv("data/donnees_hebdo.csv", sep=";", na_values="Null", low_memory=False)
weeklyd = pd.wide_to_long(weeklyd, 
                stubnames=["18/3","19/3","20/3","21/3","22/3","23/3","24/3"],
                i= "Jour", j= "Intensité")
weeklyd = weeklyd.dropna()
#On retire les deux compteurs qui sont trop loin de Montpellier Métropôle :
compteurs_todrop = weeklyd[
    (weeklyd["N° Série"] == "X2H22104765")
    & (weeklyd["N° Série"] == "X2H21070350")
].index
weeklyd.drop(compteurs_todrop, inplace=True)

weeklyd = (weeklyd.groupby(["Jour", "Latitude", "Longitude"])["Intensité"]).mean().reset_index(name="Intensité")

lundi = weeklyd[(weeklyd["Jour"] == "18/3")]
heatLundi = lundi[["Latitude", "Longitude", "Intensité"]].copy()
longitude = heatLundi["Latitude"].tolist()
latitutde = heatLundi["Longitude"].tolist()
intensity = heatLundi["Intensité"].tolist()
lundi = HeatMap(
    list(zip(latitutde, longitude, intensity)),
    name="Lundi",
    gradient=grad,
    radius=10,
    blur=35,
)
lundi = folium.FeatureGroup(name="Lundi", show=True)
lundi.add_to(lundi)

mardi = weeklyd[(weeklyd["Jour"] == "19/3")]
heatMardi = mardi[["Latitude", "Longitude", "Intensité"]].copy()
longitude = heatMardi["Latitude"].tolist()
latitutde = heatMardi["Longitude"].tolist()
intensity = heatMardi["Intensité"].tolist()
mardi = HeatMap(
    list(zip(latitutde, longitude, intensity)),
    name="Mardi",
    gradient=grad,
    radius=10,
    blur=35,
)
mari = folium.FeatureGroup(name="Mardi", show=True)
mardi.add_to(mardi)

mercredi = weeklyd[(weeklyd["Jour"] == "20/3")]
heatMerc= mercredi[["Latitude", "Longitude", "Intensité"]].copy()
longitude = heatMerc["Latitude"].tolist()
latitutde = heatMerc["Longitude"].tolist()
intensity = heatMerc["Intensité"].tolist()
mercredi = HeatMap(
    list(zip(latitutde, longitude, intensity)),
    name="Mercredi",
    gradient=grad,
    radius=10,
    blur=35,
)
mercredi = folium.FeatureGroup(name="Mercredi", show=True)
mercredi.add_to(mercredi)

jeudi = weeklyd[(weeklyd["Jour"] == "21/3")]
heatJeudi= jeudi[["Latitude", "Longitude", "Intensité"]].copy()
longitude = heatJeudi["Latitude"].tolist()
latitutde = heatJeudi["Longitude"].tolist()
intensity = heatJeudi["Intensité"].tolist()
jeudi = HeatMap(
    list(zip(latitutde, longitude, intensity)),
    name="Jeudi",
    gradient=grad,
    radius=10,
    blur=35,
)
jeudi = folium.FeatureGroup(name="Jeudi", show=True)
jeudi.add_to(jeudi)

vendredi = weeklyd[(weeklyd["Jour"] == "22/3")]
heatVend = vendredi[["Latitude", "Longitude", "Intensité"]].copy()
longitude = heatVend["Latitude"].tolist()
latitutde = heatVend["Longitude"].tolist()
intensity = heatVend["Intensité"].tolist()
vendredi = HeatMap(
    list(zip(latitutde, longitude, intensity)),
    name="Vendredi",
    gradient=grad,
    radius=10,
    blur=35,
)
vendredidi = folium.FeatureGroup(name="Vendredi", show=True)
vendredi.add_to(vendredi)

samedi = weeklyd[(weeklyd["Jour"] == "23/3")]
heatSam = samedi[["Latitude", "Longitude", "Intensité"]].copy()
longitude = heatSam["Latitude"].tolist()
latitutde = heatSam["Longitude"].tolist()
intensity = heatSam["Intensité"].tolist()
samedi = HeatMap(
    list(zip(latitutde, longitude, intensity)),
    name="Samedi",
    gradient=grad,
    radius=10,
    blur=35,
)
samedi = folium.FeatureGroup(name="Samedi", show=True)
samedi.add_to(samedi)

dimanche = weeklyd[(weeklyd["Jour"] == "24/3")]
heatDim = dimanche[["Latitude", "Longitude", "Intensité"]].copy()
longitude = heatDim["Latitude"].tolist()
latitutde = heatDim["Longitude"].tolist()
intensity = heatDim["Intensité"].tolist()
dimanche = HeatMap(
    list(zip(latitutde, longitude, intensity)),
    name="Dimanche",
    gradient=grad,
    radius=10,
    blur=35,
)
dimanche = folium.FeatureGroup(name="Dimanche", show=True)
dimanche.add_to(dimanche)

Montpellier.add_child(lundi)
Montpellier.add_child(mardi)
Montpellier.add_child(mercredi)
Montpellier.add_child(jeudi)
Montpellier.add_child(vendredi)
Montpellier.add_child(samedi)
Montpellier.add_child(dimanche)


folium.TileLayer("OpenStreetMap", name="Street Map").add_to(Montpellier)

folium.LayerControl(position="topleft", collapsed=True, opacity=0.7).add_to(Montpellier)

GroupedLayerControl(
    position="topleft",
    groups={"Jours de la semaine": [lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche]},
    collapsed=False,
).add_to(Montpellier)


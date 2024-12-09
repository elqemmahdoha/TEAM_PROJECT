import time
from map_data import load_map_interactive_data, load_coord_stations 
import folium
from folium.plugins import HeatMap, GroupedLayerControl
import branca.colormap as cm

def main():
    """"   
    Script principal pour la création d'une carte interactive de la prédiction du trafic cycliste à Montpellier.
    
    Ce script charge les données des compteurs triées pour l'analyse interactive de la carte, crée des HeatMap pour chaque jour de la semaine, ajoute des marqueurs pour les stations Velomagg, et fournit des options cliquables pour afficher les HeatMap des jours de la semaine.

    Le processus inclut les étapes suivantes :
    1. Chargement des données des compteurs triées.
    2. Création des HeatMap pour chaque jour de la semaine.
    3. Ajout des marqueurs pour les stations Velomagg.
    4. Création des options cliquables pour afficher les HeatMap des jours de la semaine.
    5. Ajout des options de visualisation de la carte.

    Modules utilisés :
    - `map_data`: Pour charger les données des compteurs triées et les coordonnées des stations Velomagg.
    - `folium`: Pour créer la carte interactive.
    - `branca`: Pour gérer la légende de la carte.
    
    Temps d'exécution : environ 1 minute.
    """
    # Initialisation de la carte avec focalisation au centre de Montpellier
    Montpellier = folium.Map(location=[43.62505, 3.862038], zoom_start=10.5, tiles=None)

    weeklyd = load_map_interactive_data()
    grad = {0: "#ffff00", 0.5: "#ffcc66", 0.8: "#aa00aa", 1: "#800080"} # Gradient de couleurs accessibles aux daltoniens
    color_mapa = cm.LinearColormap(
        colors=list(grad.values()),  
        vmin=0, vmax=weeklyd["Intensité"].max(), 
        caption="Prédiction du trafic cycliste à Montpellier",
    )
    svg_style = "<style>svg#legend {background-color: rgba(255,255,255,0.5);}</style>"
    Montpellier.get_root().header.add_child(folium.Element(svg_style))
    color_mapa.add_to(Montpellier) # Ajout de la légende

    days = ["18/3", "19/3", "20/3", "21/3", "22/3", "23/3", "24/3"]
    day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    day_feature_groups = []
    for day, day_name in zip(days, day_names): # Création des HeatMap pour chaque jour de la semaine choisie
        data = weeklyd[weeklyd["Jour"] == day]
        data["Intensité"] *= 10 # Augmentation de l'intensité pour une meilleure visibilité
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
    
        day_feature_groups.append(feature_group) # Ajout des HeatMap dans la liste des groupes de fonctionnalités (Feature Groups)

    name, lat, lon = load_coord_stations("data/files/MMM_MMM_Velomagg.json")
    # Création des marqueurs pour chaque station Velomagg avec des icônes de vélo
    folium.Marker(
        location=[lat, lon], 
        icon=folium.Icon(icon="bicycle", 
                    prefix="fa", icon_color="black", 
                    color="black", icon_size=(10, 10), 
                    shadow_size=(0,0)), 
        popup=folium.Popup(name, parse_html=True), 
    ).add_to(Montpellier)

    # Création des options cliquables pour afficher les HeatMap des jours de la semaine
    GroupedLayerControl(
        position="topleft",
        groups={"Jours de la semaine": day_feature_groups},
        collapsed=False,
    ).add_to(Montpellier)

    # Ajout des options de visualisation de la carte
    folium.TileLayer("OpenStreetMap", name="Street Map").add_to(Montpellier)
    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Satellite',
        overlay = False,
        control = True).add_to(Montpellier)
    folium.LayerControl(position="topleft", collapsed=False, opacity=0.7).add_to(Montpellier)


    # Sauvegarde de la carte interactive
    Montpellier.save("mtp_interactive.html")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Temps : {end - start:.5f} s")
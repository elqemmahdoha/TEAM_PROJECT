import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo"
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "data", "video", "compteurs")  # Répertoire local pour stocker les fichiers

def scrape_json_and_geojson_links():
    """
    Scraper la page de données pour trouver les liens vers les fichiers JSON et GeoJSON.

    Cette fonction récupère le contenu HTML de la page spécifiée par `BASE_URL`, 
    puis recherche tous les liens qui se terminent par `.json` ou `.geojson`.

    Retourne:
        list: Une liste des liens vers les fichiers JSON et GeoJSON trouvés sur la page.
    
    Lève:
        RuntimeError: Si la page n'est pas accessible (code de statut HTTP autre que 200).
    """
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        raise RuntimeError(f"Impossible d'accéder à {BASE_URL} : {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    
    # Recherche des liens vers les fichiers JSON et GeoJSON
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".json") or href.endswith(".geojson"):  # Filtre pour les fichiers JSON et GeoJSON
            links.append(href)
    
    return links

def download_file(url, filename):
    """
    Télécharge un fichier à partir d'une URL et l'enregistre localement.

    Cette fonction télécharge un fichier depuis l'URL spécifiée et l'enregistre dans le dossier 
    local défini par `DOWNLOAD_FOLDER` sous le nom de fichier spécifié. Si le fichier existe déjà, 
    il ne sera pas téléchargé à nouveau.

    Arguments:
        url (str): L'URL du fichier à télécharger.
        filename (str): Le nom du fichier tel qu'il doit être enregistré localement.
    """
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if not os.path.exists(filepath):  # Ne télécharger que si le fichier n'existe pas déjà
        print(f"Téléchargement de {filename}...")
        response = requests.get(url)
        with open(filepath, "wb") as file:
            file.write(response.content)
    else:
        print(f"{filename} existe déjà, téléchargement ignoré.")

def download_files(links):
    """
    Télécharge tous les fichiers JSON et GeoJSON à partir des liens fournis.

    Cette fonction crée d'abord le dossier de téléchargement local si nécessaire, puis
    télécharge chaque fichier trouvé via les liens donnés en argument. Chaque fichier est
    téléchargé et enregistré dans `DOWNLOAD_FOLDER`.

    Arguments:
        links (list): Liste des URLs des fichiers JSON et GeoJSON à télécharger.
    """
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Créer le dossier si nécessaire
    for link in links:
        filename = os.path.basename(link)
        download_file(link, filename)

def fetch_all_files():
    """
    Récupère tous les fichiers JSON et GeoJSON à partir des liens scrappés.

    Cette fonction appelle la fonction `scrape_json_and_geojson_links` pour obtenir tous les liens
    vers les fichiers JSON et GeoJSON disponibles sur la page cible, puis elle utilise `download_files`
    pour télécharger ces fichiers localement.

    Utilisation:
        fetch_all_files()  # Récupérer et télécharger tous les fichiers JSON et GeoJSON
    """
    links = scrape_json_and_geojson_links()
    download_files(links)  # Télécharger tous les fichiers JSON et GeoJSON

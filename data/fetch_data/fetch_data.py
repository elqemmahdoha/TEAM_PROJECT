import os
import requests
from bs4 import BeautifulSoup

# URLs des pages à scraper
BASE_URL1 = "https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo"
BASE_URL2 = "https://data.montpellier3m.fr/dataset/courses-des-velos-velomagg-de-montpellier-mediterranee-metropole"
BASE_URL3 = "https://data.montpellier3m.fr/dataset/stations-velomagg-de-montpellier-m%C3%A9diterran%C3%A9e-m%C3%A9tropole"

# Répertoire local pour stocker les fichiers
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "data", "files")

def scrape_links(base_url, file_extensions):
    """
    Scraper la page de données pour trouver les liens vers des fichiers avec des extensions spécifiques.

    Arguments:
        base_url (str): URL de la page à scraper.
        file_extensions (list): Liste des extensions de fichiers à rechercher (par ex. ['.json', '.geojson', '.csv']).

    Retourne:
        list: Une liste des liens vers les fichiers trouvés.

    Lève:
        RuntimeError: Si la page n'est pas accessible (code de statut HTTP autre que 200).
    """
    response = requests.get(base_url)
    if response.status_code != 200:
        raise RuntimeError(f"Impossible d'accéder à {base_url} : {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if any(href.endswith(ext) for ext in file_extensions):  # Vérifie les extensions spécifiées
            links.append(href)
    
    return links

def download_file(url, filename):
    """
    Télécharge un fichier à partir d'une URL et l'enregistre localement.

    Arguments:
        url (str): L'URL du fichier à télécharger.
        filename (str): Le nom du fichier tel qu'il doit être enregistré localement.
    """
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        print(f"Téléchargement de {filename}...")
        response = requests.get(url)
        with open(filepath, "wb") as file:
            file.write(response.content)
    else:
        print(f"{filename} existe déjà, téléchargement ignoré.")

def download_files(links):
    """
    Télécharge tous les fichiers à partir des liens fournis.

    Arguments:
        links (list): Liste des URLs des fichiers à télécharger.
    """
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    for link in links:
        filename = os.path.basename(link)
        download_file(link, filename)

def fetch_all_files():
    """
    Récupère et télécharge tous les fichiers JSON, GeoJSON et CSV des pages cibles.
    """
    # Scraping des fichiers JSON et GeoJSON pour écocompteurs
    compteurs_json_geojson_links = scrape_links(BASE_URL1, ['.json', '.geojson'])
    # Scraping du fichier CSV Courses Velomagg
    courses_csv_links = scrape_links(BASE_URL2, ['.csv'])
    # Scraping fu fichier JSON pour Stations Velomagg 
    stations_json_links = scrape_links(BASE_URL3,['.json'])
    
    # Téléchargement de tous les fichiers Json et Geojson compteurs 
    print("Téléchargement des fichiers JSON et GeoJSON des écocompteurs...")
    download_files(compteurs_json_geojson_links)
    
    # Téléchargement fichier CSV Courses Velomagg 
    print("Téléchargement fichier CSV Courses Velomagg...")
    download_files(courses_csv_links)

    # Téléchargement fichier Json Stations Velomagg 
    print("Téléchargement fichier JSON Stations Velomagg...")
    download_files(stations_json_links)

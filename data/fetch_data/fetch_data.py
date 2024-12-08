import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo"
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "data", "video", "compteurs")  # Répertoire local pour stocker les fichiers

def scrape_json_and_geojson_links():
    """Scraper la page pour trouver les liens des fichiers JSON et GeoJSON."""
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
    """Télécharger un fichier à partir d'une URL et l'enregistrer localement."""
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if not os.path.exists(filepath):  # Ne télécharger que si le fichier n'existe pas déjà
        print(f"Téléchargement de {filename}...")
        response = requests.get(url)
        with open(filepath, "wb") as file:
            file.write(response.content)
    else:
        print(f"{filename} existe déjà, téléchargement ignoré.")

def download_files(links):
    """Télécharger tous les fichiers JSON et GeoJSON à partir des liens scrappés."""
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Créer le dossier si nécessaire
    for link in links:
        filename = os.path.basename(link)
        download_file(link, filename)

def fetch_all_files():
    """Récupérer tous les fichiers JSON et le fichier GeoJSON."""
    links = scrape_json_and_geojson_links()
    download_files(links)  # Télécharger tous les fichiers JSON et GeoJSON

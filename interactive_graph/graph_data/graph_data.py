import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
# Définition d'une fonction pour corriger l'encodage des caractères
def correct_encoding(value):
    """
    Fonction pour corriger l'encodage des caractères.
    
    Parameters
    ----------
    value : str
        Valeur à corriger
        
    Returns
    -------
        str
        Valeur corrigée
    """
    if isinstance(value, str):
        return value.encode("latin1", errors="replace").decode("utf-8", errors="replace")
    return value

def load_graph_data():
    """
    Chargement des données pour les graphiques interactifs.

    Returns
    -------
    pd.DataFrame
        Données des courses Velomagg
    dict
        Dictionnaire pour associer les jours de la semaine aux dates en français
    """
    # Importation des données des courses Velomagg
    rd_velomagg = pd.read_csv("data/video/courses/TAM_MMM_CoursesVelomagg.csv", encoding="utf-8-sig")
    # Correction de l'encodage des caractères pour faire disparaître les caractères spéciaux
    rd_velomagg = rd_velomagg.apply(lambda col: col.apply(correct_encoding) if col.dtype == "object" else col)

    rd_velomagg["Date"] = pd.to_datetime(rd_velomagg["Departure"]).dt.date
    # Choix des dates de la semaine à visualiser (mêmes dates que celles des données des compteurs)
    date_debut = pd.to_datetime("2024-03-18").date()
    date_fin = pd.to_datetime("2024-03-24").date()

    rd_velomagg = rd_velomagg[(rd_velomagg["Date"] >= date_debut) & (rd_velomagg["Date"] <= date_fin)]
    dates = pd.date_range(date_debut, date_fin).date # Création de la liste des dates de la semaine
    weekdays = {date.strftime("%A"): date for date in dates} # Création d'un dictionnaire pour associer les jours de la semaine aux dates en français
    return rd_velomagg, weekdays

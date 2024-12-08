import pandas as pd

def charger_csv(input_file: str) -> pd.DataFrame:
    """
    Charge un fichier CSV avec gestion de l'encodage BOM (si présent).

    Arguments:
        input_file (str): Le chemin du fichier CSV à charger.

    Retourne:
        pd.DataFrame: Le DataFrame chargé à partir du fichier CSV.
    """
    try:
        df = pd.read_csv(input_file, encoding="utf-8-sig")  # 'utf-8-sig' permet de lire un fichier avec BOM
    except UnicodeDecodeError:
        print("Encodage utf-8-sig incorrect. Essayez un autre encodage, comme latin1.")
        raise
    return df

def correct_encoding(value) -> str:
    """
    Corrige les erreurs d'encodage pour chaque chaîne de caractères.
    
    Arguments:
        value: La valeur à corriger (peut être une chaîne de caractères ou autre).

    Retourne:
        str: La chaîne de caractères corrigée.
    """
    if isinstance(value, str):
        # Utilisation de 'replace' pour corriger les caractères mal encodés
        return value.encode("latin1", errors="replace").decode("utf-8", errors="replace")
    return value

def corriger_encodage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique la correction d'encodage uniquement aux colonnes de type "object" (chaînes de caractères).
    
    Arguments:
        df (pd.DataFrame): Le DataFrame à corriger.

    Retourne:
        pd.DataFrame: Le DataFrame avec les colonnes de type "object" corrigées.
    """
    return df.apply(lambda col: col.apply(correct_encoding) if col.dtype == "object" else col)

def filtrer_donnees(df: pd.DataFrame, date_debut: str) -> pd.DataFrame:
    """
    Filtre les données en fonction de la date de départ, supprime les lignes avec des stations identiques 
    et nettoie certaines stations spécifiques.
    
    Arguments:
        df (pd.DataFrame): Le DataFrame contenant les données à filtrer.
        date_debut (str): La date de début sous format 'YYYY-MM-DD' pour le filtrage.

    Retourne:
        pd.DataFrame: Le DataFrame filtré.
    """
    # Convertir la colonne 'Departure' en type datetime
    df["Departure"] = pd.to_datetime(df["Departure"], errors="coerce")  # Ignorer les valeurs invalides

    # Filtrer pour garder uniquement les lignes à partir du 1er août 2024
    df_filtered = df[df["Departure"] >= date_debut]

    # Supprimer les lignes où 'Departure station' et 'Return station' sont identiques
    df_filtered = df_filtered[df_filtered["Departure station"] != df_filtered["Return station"]]

    # Supprimer les lignes où 'Return station' est vide ou NaN
    df_filtered = df_filtered[df_filtered["Return station"].notna() & (df_filtered["Return station"] != "")]

    # Supprimer les lignes où 'Departure station' ou 'Return station' contient "Pérol"
    df_filtered = df_filtered[~df_filtered["Departure station"].str.contains("055 Pérols Etang de l'Or", case=False, na=False)]
    df_filtered = df_filtered[~df_filtered["Return station"].str.contains("055 Pérols Etang de l'Or", case=False, na=False)]
    df_filtered = df_filtered[~df_filtered["Departure station"].str.contains("058 Perols etang or", case=False, na=False)]
    df_filtered = df_filtered[~df_filtered["Return station"].str.contains("058 Perols etang or", case=False, na=False)]

    # Extraire les numéros avant les stations pour les deux colonnes
    df_filtered['Departure number'] = df_filtered['Departure station'].str.extract(r'(\d+)')[0].str.lstrip('0')
    df_filtered['Return number'] = df_filtered['Return station'].str.extract(r'(\d+)')[0].str.lstrip('0')

    # Supprimer les numéros et ne garder que le nom des stations
    df_filtered['Departure station'] = df_filtered['Departure station'].str.replace(r'^\d+\s+', '', regex=True)
    df_filtered['Return station'] = df_filtered['Return station'].str.replace(r'^\d+\s+', '', regex=True)

    # Supprimer les lignes où Departure number' ou 'Return number' contient "60" (Comedie Baudin)
    df_filtered = df_filtered[~df_filtered["Departure number"].str.contains("60", case=False, na=False)]
    df_filtered = df_filtered[~df_filtered["Return number"].str.contains("60", case=False, na=False)]

    # Supprimer les lignes où Departure number' ou 'Return number' contient "98" (AtelierTAM)
    df_filtered = df_filtered[~df_filtered["Departure number"].str.contains("98", case=False, na=False)]
    df_filtered = df_filtered[~df_filtered["Return number"].str.contains("98", case=False, na=False)]

    return df_filtered

def sauvegarder_csv(df: pd.DataFrame, output_file: str):
    """
    Sauvegarde le DataFrame filtré dans un fichier CSV avec encodage utf-8-sig (sans BOM).
    
    Arguments:
        df (pd.DataFrame): Le DataFrame à sauvegarder.
        output_file (str): Le chemin du fichier CSV de sortie.
    """
    df.to_csv(output_file, index=False, encoding="utf-8-sig")  # Utilisation de utf-8-sig pour sauvegarder sans BOM

import pandas as pd

# Chemins des fichiers
input_file = "data\\video\\courses\\TAM_MMM_CoursesVelomagg.csv"
output_file = "data\\video\\courses\\CoursesVelomagg_filtre.csv"

# Lire le fichier CSV avec un encodage explicite et gérer le BOM (s'il y en a)
try:
    df = pd.read_csv(input_file, encoding="utf-8-sig")  # 'utf-8-sig' permet de lire un fichier avec BOM
except UnicodeDecodeError:
    print("Encodage utf-8-sig incorrect. Essayez un autre encodage, comme latin1.")
    raise

# Correction des erreurs d'encodage pour chaque chaîne de caractères
def correct_encoding(value):
    if isinstance(value, str):
        # Utilisation de 'replace' pour corriger les caractères mal encodés
        return value.encode("latin1", errors="replace").decode("utf-8", errors="replace")
    return value

# Appliquer la correction d'encodage uniquement aux colonnes de type "object"
df = df.apply(lambda col: col.apply(correct_encoding) if col.dtype == "object" else col)

# Convertir la colonne 'Departure' en type datetime
df["Departure"] = pd.to_datetime(df["Departure"], errors="coerce")  # Ignorer les valeurs invalides

# Filtrer pour garder uniquement les lignes à partir du 1er septembre 2024
df_filtered = df[df["Departure"] >= "2024-08-01"]

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

# Sauvegarder le fichier corrigé, filtré et sans lignes où les stations sont identiques
df_filtered.to_csv(output_file, index=False, encoding="utf-8-sig")  # Utilisation de utf-8-sig pour sauvegarder sans BOM
import os
import plotly.express as px

def creer_figure_polaire(polar_data, chemin_polar_figure):
    """Crée et enregistre la figure polaire des intensités moyennes par mois."""
    if os.path.exists(chemin_polar_figure):
        print(f"Le fichier {chemin_polar_figure} existe déjà.")
    else: 
        fig = px.line_polar(
            polar_data, 
            r='Intensity', 
            theta='Month', 
            color='Nom du com',
            line_close=True,
            range_r=[0,2500],
            start_angle=0,
            title="Intensité moyenne des compteurs par mois"
        )
        fig.write_html(chemin_polar_figure)

def creer_figure_intensite_moyenne(tableau_moyennes, chemin_average_intensity):
    """Crée et enregistre le graphique de l'intensité moyenne des passages."""
    if os.path.exists(chemin_average_intensity):
        print(f"Le fichier {chemin_average_intensity} existe déjà.")
    else:
        fig = px.line(tableau_moyennes, x='Month', y='Average Intensity', 
                      markers=True, title="Passage moyen devant les éco-compteurs par mois sur l'année 2024")
        fig.update_traces(line=dict(color='darkviolet'))
        fig.update_layout(
            xaxis_title="Mois",
            yaxis_title="Intensité de passage moyenne",
            template="plotly_white",
            showlegend=True
        )
        fig.write_html(chemin_average_intensity)

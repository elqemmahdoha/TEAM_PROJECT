import time
from graph import plot_interactive_graph

def main():
    """
    Script principal pour la création d'un graphique interactif pour visualiser les retraits et dépôts des Vélomaggs.

    Ce script charge les données des courses Velomagg pour l'analyse interactive du graphique, crée des barres pour les retraits et dépôts des Vélomaggs, et fournit des options cliquables pour afficher les données des jours de la semaine.

    Le processus inclut les étapes suivantes :
    1. Chargement des données des courses Velomagg.
    2. Création des barres pour les retraits et dépôts des Vélomaggs.
    3. Ajout des options cliquables pour afficher les données des jours de la semaine.
    4. Ajout des options de visualisation du graphique.

    Modules utilisés :
    - `graph`: Pour créer le graphique interactif.

    Temps d'exécution : environ 1 minute.
    """
    plot_interactive_graph(selected_day="lundi", show="both")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Temps : {end - start:.5f} s")
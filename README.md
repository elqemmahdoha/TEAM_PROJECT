<h1 style="text-align: center;">Pédaler à Montpellier</h1>

Bienvenue sur la page source du projet **Pédaler à Montpellier** !

---

## 📚 Description du projet 

Dans le cadre du module **HAX712X - Développement logiciel** du Master Statistique et Science des Données de l'Université de Montpellier, ce projet vise à :  
- Observer le trafic cycliste dans la ville de Montpellier à partir des données fournies par Montpellier Méditerranée Métropole.  
- Prédire le trafic cycliste pour les jours à venir grâce à des algorithmes de modélisation.  

---

## 📊 Sources 

Les données utilisées dans ce projet proviennent des ressources suivantes :  
- [Open Data 3M](https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo)  
- [OpenStreetMap](https://www.openstreetmap.org/#map=6/46.45/2.21)  

Elles sont stockées dans le dossier `data` du projet pour un accès simplifié.  

---

## 🌐 Site web 

Le site internet du projet est disponible à l'URL suivante :  
➡️ [https://elqemmahdoha.github.io/TEAM_PROJECT/](https://elqemmahdoha.github.io/TEAM_PROJECT/)

---

## 💻 Code pour construire le projet 

Pour exécuter ce projet localement et construire le site web, suivez les étapes ci-dessous :  

### Étape 1 : Cloner le dépôt 
Commencez par cloner le dépôt GitHub sur votre machine locale :  
```bash
git clone https://github.com/elqemmahdoha/TEAM_PROJECT.git
cd TEAM_PROJECT
```
### Étape 2 : Créer un environnement virtuel (optionnel, recommandé)
Pour éviter les conflits de dépendances, il est recommandé de créer un environnement virtuel avec `conda` ou `venv`.

 - Pour `conda` : 
```bash
conda create -n montpellier_velo python=3.9 -y
conda activate montpellier_velo
```
 - Pour `venv` : 
```bash
python -m venv env
source env/bin/activate  # Sous Linux/Mac
env\Scripts\activate     # Sous Windows
```
### Étape 3 : Installer les dépendances 
Installez les bibliothèques nécessaires à l'aide du fichier `requirements.txt` :
```bash
conda install --file requirements.txt
```
ou
```bash
pip install -r requirements.txt
```
Vous disposez désormais de tous les éléments nécessaires pour utiliser notre projet. 

### Étape 4 : Installer les datas
L'utilisation des modules `interactive_graph`, `interactive_map`, `stats`, et `video` nécessite l’installation préalable des données nécessaires à leur bon fonctionnement. Pour cela, placez-vous à la racine du projet et exécutez la commande suivante : 
```bash
python -m data.main
```
Le temps d'exécution sera d'environ 45 secondes. 
Une fois cette étape terminée, vous pourrez pleinement exploiter et explorer les modules disponibles. Chaque module dispose de sa propre documentation, et des instructions détaillées pour leur utilisation sont fournies dans les sous-répertoires correspondants. 

### Étape 5 : Désactiver et supprimer l'environnement (facultatif)
Si vous souhaitez désactiver et supprimer l'environnement créé, suivez ces étapes :  

- Pour `conda` :

```bash
conda deactivate
```

```bash
conda remove --name montpellier_velo --all
```

- Pour `venv` :

```bash
deactivate
```

```bash
rm -rf env #Sous Linux/Mac
rmdir /s /q env #Sous Windows 
```

--- 

## 👩‍💻 Auteurs 

- [**Laura CLETZ**](https://github.com/lcletz)  
- [**Doha EL QEMMAH**](https://github.com/elqemmahdoha)  
- [**Louison GILLET**](https://github.com/LouisonGillet)  

---
## 🔏 Documentation

La documentation détaillée, générée par Sphinx est accessible [**ici**](http://127.0.0.1:5500/docs2/build/html/index.html).

---
## 📄 Licence 

Ce projet est sous licence **MIT**.  
Pour plus d'informations, veuillez consulter le fichier [LICENSE](https://github.com/elqemmahdoha/TEAM_PROJECT/blob/main/LICENSE).  

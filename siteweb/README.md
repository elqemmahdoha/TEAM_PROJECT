Ce dossier contient tous les fichiers nécessaires à la génération du site web avec Quarto, afin de rendre le site multilingue (français et anglais). 
Veuillez suivre les étapes ci-dessous dans l'ordre, depuis votre terminal :

Étape 1:
Accédez au dossier du siteweb en spécifiant son chemin:
```bash
cd siteweb  
```

Étape 2:
Exécutez les commandes suivantes pour générer le site pour chaque langue :
```bash
quarto render --profile fr0
```
```bash
quarto render --profile fr 
```
```bash
quarto render --profile en
```

Étape 3:
Vous pouvez accéder au dossier docs et ouvrir le fichier index.html pour naviguer sur le site web.
Ce dossier contient tous les fichiers nécessaires à la génération du site web avec Quarto, afin de rendre le site multilingue (français et anglais). 
Veuillez suivre les étapes ci-dessous dans l'ordre, depuis votre terminal :

Étape 1:
cd sitewe: Accédez au dossier du siteweb en spécifiant son chemin.

Étape 2:
Exécutez les commandes suivantes pour générer le site pour chaque langue :
quarto render --profile fr0 : pour générer la version française initiale du site.
quarto render --profile fr : pour générer la version complète en français.
quarto render --profile en : pour générer la version anglaise du site.

Étape 3:
Vous pouvez accéder au dossier docs et ouvrir le fichier index.html pour naviguer sur le site web.
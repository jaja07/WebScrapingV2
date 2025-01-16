# WebScrappingV2 : Comparaison des prix de maillots de football
 
Ce projet a pour but de comparer les prix des maillots de football sur trois sites internet : Nike, Unisport et Foot.fr. Il utilise `Scrapy` pour le scraping des sites web et `Docker` pour la conteneurisation. Le système est constitué de trois conteneurs principaux :
 
- **mysqlServer**: Une base de données MySQL.
- **scraper**: S'occupe du scraping des données sur les sites web mentionnés.
- **Flask**: Gère l'interface web où les données récupérées sont affichées.

## Projet en local

Pour cloner le projet sur votre ordinateur, allez dans votre terminal et saissisez la commande :

```
git clone https://github.com/jaja07/WebScrapingV2.git
``` 
## Exécution du Projet
 
Pour démarrer le projet, suivez les étapes suivantes utilisez la commande suivante :
- Assurer vous que le dossier db/db_dir/ soit supprimé. Il sera recréé après chaque exécution et devra être supprimé avant toute exécution 
- Placer vous à la racine du projet et lancer les commandes suivantes :
```
docker-compose build
``` 
```
docker-compose up -d 
```

 
## Accès à l'Interface Web
 
Pour accéder à l'interface web, ouvrez le navigateur de votre choix et visitez :
 
`localhost:8080`
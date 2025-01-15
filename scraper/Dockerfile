FROM python:3.11

WORKDIR /scraper

# Copiez uniquement le fichier requirements.txt dans le conteneur pour éviter de cacher inutilement les couches du Docker cache
COPY ./requirements.txt /scraper/

# Installez les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
# RUN rm /scraper/requirements.txt

RUN apt update
RUN apt install wait-for-it

# Copiez le reste des fichiers de l'application dans le conteneur
COPY . /scraper

# Changez le répertoire de travail pour pointer directement sur le dossier items
WORKDIR /scraper/scraping

# Définissez la commande par défaut pour exécuter le scraper
# CMD ["scrapy", "crawl", "foot_fr_spider"]
# CMD ["wait-for-it", "my:3306", "--timeout=120", "--", "scrapy", "crawl", "fvs"]

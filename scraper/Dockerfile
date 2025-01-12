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

# Définissez la commande par défaut pour exécuter le scraper
# CMD ["python", ""]


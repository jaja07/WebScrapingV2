FROM python:3.11

WORKDIR /scraper

# Copiez uniquement le fichier requirements.txt dans le conteneur pour éviter de cacher inutilement les couches du Docker cache
COPY requirements.txt /app/

# Installez les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste des fichiers de l'application dans le conteneur
COPY . /scrapper

# Définissez la commande par défaut pour exécuter l'application Flask
CMD []


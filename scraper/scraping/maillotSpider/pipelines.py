# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import MySQLdb.cursors
from itemadapter import ItemAdapter
import mysql.connector
from maillotSpider import settings  
from twisted.enterprise import adbapi
from scrapy import signals
import logging
import time
import pandas as pd

    
class MySQLPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    def __init__(self, stats):
        self.stats = stats
        self.dbpool = None
        self._connect_to_database()

    def _connect_to_database(self):
        retries = 0
        max_retries = 5  # Nombre maximal de tentatives de reconnexion
        delay = 5  # Délai en secondes entre les tentatives
 
        while retries < max_retries:
            try:
                self.dbpool = adbapi.ConnectionPool('MySQLdb',
                    host=settings.MYSQL_HOST,
                    user=settings.MYSQL_USER,
                    passwd=settings.MYSQL_PASS,
                    db=settings.MYSQL_DB,
                    charset='utf8',
                    use_unicode=True,
                    cursorclass=MySQLdb.cursors.DictCursor
                )
                return  # Connexion réussie, sortez de la boucle
            except Exception as e:
                retries += 1
                logging.error(f"Tentative de connexion {retries}/{max_retries} échouée: {e}")
                time.sleep(delay)
 
        if retries == max_retries:
            logging.error("Échec de toutes les tentatives de connexion à la base de données.")
            # Gérer l'échec ici (par exemple, en arrêtant le spider ou en levant une exception)

    def open_spider(self, spider):
        self.items = []

    def spider_closed(self, spider):
        # À la fin du spider, convertir la liste des articles en DataFrame
        df = pd.DataFrame(self.items)
        # Afficher la DataFrame
        print(df[['seller', 'product_url']])
        self.dbpool.close()
        # Vous pouvez aussi sauvegarder la DataFrame dans un fichier si nécessaire
        # df.to_csv('output.csv', index=False)

    def process_item(self, item, spider):
        
        # Supprimez l'espace insécable, le symbole euro, et remplacez la virgule par un point.
        price_str = item['prix']
        if isinstance(price_str, list):
            price_str = price_str[0]  # Si la liste est vide, cela lèvera une erreur.
        price_str = price_str.replace('€', '').replace('\xa0', '').replace(',', '.').strip()

        # Supprimez tous les espaces restants et convertissez en float.
        try:
            item['prix'] = float(price_str)
        except ValueError as e:
            # Gérez l'erreur ou imprimez un message pour déboguer
            spider.logger.error(f"Erreur de conversion: {e}, Valeur de l'item: {price_str}")
            item['prix'] = None  # ou une autre valeur par défaut si nécessaire
        annee = item['nom'].split()
        for chaine in annee:
            if chaine.startswith('20'):
                item['annee'] = chaine
        
        self.items.append(item)
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):
        # Ajoutez ici les champs correspondants à votre item
        fields = ['nom', 'prix','lien','annee','sites', 'img']
        # ... dans votre méthode _insert_record ...
        values = [str(item.get(field)) for field in fields]
        # Prenez le premier élément de chaque liste
        values = ['"'+value+'"' for value in values]  # Assurez-vous que les valeurs sont des chaînes
        result = tx.execute(
            """ INSERT IGNORE INTO maillots ({}) VALUES ({}) """\
            .format(','.join(fields), ','.join(values))
        )
        print("MYSQL: ", result)
        if result > 0:
            self.stats.inc_value('database/items_added')
   
    def _handle_error(self, e):
        logging.error(e)

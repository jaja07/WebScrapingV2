# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItemsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nom = scrapy.Field()
    prix = scrapy.Field()
    lien = scrapy.Field()
    annee = scrapy.Field()
    img=scrapy.Field()
    sites = scrapy.Field()
    

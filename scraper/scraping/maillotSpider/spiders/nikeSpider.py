import scrapy
from ..items import ItemsItem


class NikespiderSpider(scrapy.Spider):
    name = "nikeSpider"
    allowed_domains = ["nike.com"]
    start_urls = ["https://www.nike.com/fr/w/hommes-football-maillots-dequipe-1gdj0z3a41eznik1"]

    def parse(self, response):
        jerseys=response.xpath('//main/section/div/div')
        for j in jerseys:
         
            maillot = ItemsItem()
            maillot['lien'] = j.xpath('./div/figure/a[@class="product-card__link-overlay"]/@href').get().strip()
            maillot['nom'] = j.xpath('./div/figure/div/div/div[@class="product-card__titles"]/div[@class="product-card__title"]/text()').get()
            maillot['prix'] = j.xpath('./div/figure/div/div[@class="product-card__animation_wrapper"]/div/div/div/div[contains(@class, "is--current-price css")]/text()').get()
            maillot['sites'] = 'nike.com'
            maillot['img']=j.xpath('./div/figure/a[@class="product-card__img-link-overlay"]/div[@class="wall-image-loader  css-1la3v4n"]/img/@src').get()
            yield maillot

        
        
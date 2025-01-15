import scrapy
from ..items import ItemsItem

class UnisportspiderSpider(scrapy.Spider):
    name = "unisportspider"
    allowed_domains = ["unisportstore.fr"]
    start_urls = ["https://www.unisportstore.fr/maillots-de-football/"]

    def parse(self, response):       
        items = response.xpath('//article[@class="relative rounded-lg bg-white @container z-[10] w-full p-2"]/a')
        for item in items:
            lien = item.xpath('./@href').get()
            yield response.follow(lien, self.parse_maillots)


    def parse_maillots(self, response):
        article = ItemsItem()
        article['nom'] = response.xpath('//div[@class="p-4 lg:col-span-2 lg:px-0 lg:py-12"]/h1/text()').get()
        if response.xpath('//span[@class="font-semibold"]/text()').get():
            article['prix'] = response.xpath('//span[@class="font-semibold"]/text()').get().strip()
        article['lien'] = response.url
        article['sites'] = 'unisportstore.fr'
        yield article

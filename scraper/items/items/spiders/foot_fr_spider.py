import scrapy
from ..items import ItemsItem


class FootFrSpiderSpider(scrapy.Spider):
    name = "foot_fr_spider"
    allowed_domains = ["foot.fr"]
    start_urls = ["https://www.foot.fr/maillots-145"]

    

    def parse(self, response):
        items = response.xpath('//div[@class="c-pdt-mini__body"]/p/a')
        for item in items:
            lien = item.xpath('./@href').get()
            yield response.follow(lien, self.parse_lien)
            
        
        #suivante = response.xpath('//li[@class="next"]/a/@href').get()
        #if suivante is not None:
            #lien = response.urljoin(suivante)
            #yield scrapy.Request(lien)

    

    def parse_lien(self, response):
        
        article = ItemsItem()
        article['nom'] = response.xpath('//h1[@class="c-pdt__title"]/text()').get()
        if response.xpath('//span[@class="c-price--lg--discount u-mr-2"]/text()').get():
            article['prix'] = response.xpath('//span[@class="c-price--lg--discount u-mr-2"]/text()').get().strip()
        else:
            article['prix'] = response.xpath('//span[@class="c-price--lg u-mr-2"]/text()').get().strip()
        #item['prix'] = response.xpath('//p[@class="product-price__content c-text c-text--size-m c-text--style-subtitle c-text--bold c-text--spacing-default"]/text()').get()+response.xpath('//p[@class="product-price__content c-text c-text--size-s c-text--style-p c-text--bold c-text--spacing-default"]/text()').get()
        #item['description'] = response.xpath('//div[@class="product-content__content c-text c-text--size-s c-text--style-p c-text--spacing-default"]/div/text()').get()
        article['lien'] = response.url
        yield article

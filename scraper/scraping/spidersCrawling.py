from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from maillotSpider.spiders.foot_fr_spider import FootFrSpiderSpider
from maillotSpider.spiders.nikeSpider import NikespiderSpider
from maillotSpider.spiders.unisportspider import UnisportspiderSpider
def run_spiders():
    
    process = CrawlerProcess(get_project_settings())
    process.crawl(FootFrSpiderSpider)
    process.crawl(NikespiderSpider)
    process.crawl(UnisportspiderSpider)
    process.start()
if __name__ == "__main__":
    run_spiders()
    import logging



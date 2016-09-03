import re

from scrapy.spiders import Spider
#from scrapy.selector import HtmlXPathSelector
#from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from tutorialScrapy.items import CategoryItem


class CategoryLoader(ItemLoader):
    default_output_processor = TakeFirst()


class CategorySpider(Spider):
    name = "category"
    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorialScrapy.pipelines.JSONPipeline': 400
            #'tutorialScrapy.pipelines.MySQLStoreProductPipeline': 400
        }
    }
    allowed_domains = ["buyincoins.ru"]
    start_urls = [
        "http://www.buyincoins.ru/",
    ]

    def parse(self, response):

        #for cat in response.selector.xpath('//a[@href="/c/Computers-Networking_4.html"]/following-sibling::ul[@class="dropdown-menu"]/li'):
        for cat in response.selector.xpath('//li[@class="dropdown"]'):

            loader = CategoryLoader(CategoryItem(), selector=cat)
            loader.add_xpath('title', 'a/text()')
            loader.add_xpath('url', 'a/@href')
            loader.add_value('category_id', 0)
            yield loader.load_item()


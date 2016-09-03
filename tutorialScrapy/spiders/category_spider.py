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
            'tutorialScrapy.pipelines.JsonExportPipeline': 400
            #'tutorialScrapy.pipelines.MySQLStoreProductPipeline': 400
        },
        'OUT_FILE': 'category.json'
    }
    allowed_domains = ["buyincoins.ru"]
    start_urls = [
        "http://www.buyincoins.ru/sitemap.html",
    ]

    def parse(self, response):

        #for cat in response.selector.xpath('//a[@href="/c/Computers-Networking_4.html"]/following-sibling::ul[@class="dropdown-menu"]/li'):
        s = response.selector.xpath('//div[@class="wrap content rounded"]/div[@class="sitemap_line"]')
        l = len(s)
        for cat in s:
            main_category = cat.xpath('a/text()').extract()
            m = cat.xpath('div[@class="sitemap_category"]/a')
            k = len(m)
            for subcat in cat.xpath('div[@class="sitemap_category"]/a[contains(@href, "/c/")]'):
                loader = CategoryLoader(CategoryItem(), selector=subcat)
                loader.add_xpath('title', 'text()')
                loader.add_xpath('url', '@href')
                loader.add_value('main_category', main_category)
                #loader.add_value('category_id', 0)
                yield loader.load_item()


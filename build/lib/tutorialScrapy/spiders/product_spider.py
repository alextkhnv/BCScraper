import re

from scrapy import Request
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.linkextractors import LinkExtractor
from tutorialScrapy.items import ProductItem, CategoryItem
from scrapy.conf import settings


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ProductSpider(CrawlSpider):
    category_name = settings['CATEGORY_NAME']
    category_id = settings['CATEGORY_ID']

    def __init__(self, category_name=None, category_id=None, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.category_name = category_name
        self.category_id = category_id

    name = "product"
    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorialScrapy.pipelines.JsonExportPipeline': 400
            #'tutorialScrapy.pipelines.MySQLStoreProductPipeline': 400
        }
    }
    allowed_domains = ["buyincoins.ru"]
    start_urls = [
        "http://www.buyincoins.ru/sitemap.html",
    ]

    category_list_xpath = '//div[@class="sitemap_line"]/a[@class="sitemap_title"]/following-sibling::div[@class="sitemap_category"]/a'
    item_list_xpath = '//li[@class="viewPics"]/p[@class="p-title"]/a[@target]/@href'
    #deals_list_xpath = '//li[@class="viewPics"]'
    media_list_xpath = '//div[@class="desc product_clear"]'
    desc_table_list_xpath = '//div[@class="desc product_clear"]//table/tbody/tr'
    item_fields = {
        'title':     './/div[@class="info r"]/div[@class="block"]/h1/text()',
        'cost_usd':  './/div[@class="info r"]/div[@class="block price"]/table/tr/td[@class="currPrice"]/text()',
        'item_code': './/div[@class="info r"]/div[@class="block"]/div[@class="r"]/text()',
        'sku':       './/div[@class="info r"]/div[@class="block price"]/div[@class="pull-right"]/span[@id="attr-sku"]/text()',
        'status':    './/div[@class="info r"]/div[@class="block prodInfo"]/div[contains(@class, "stockStatus")]/text()',
        'category':  './/ul[@class="breadcrumb"]/li[2]/a/text()',
    }

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(LinkExtractor(allow=('/c/Tablets-eReaders_356', ), deny=('sitemap\.html', )), ),

        #Rule(LinkExtractor(allow=('([A-Z][a-z]+(-|_))+\d+.html', '([A-Z][a-z]+(-|_))+\d+_p\d+.html', ))),
        Rule(LinkExtractor(allow=('/c/Tablets-eReaders_356.html', '/c/Tablets-eReaders_356_p\d+.html', ))),
        #Rule(LinkExtractor(allow=('/c/Tablets-eReaders_356.html', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(LinkExtractor(allow=('item/\d+', )), callback='parse_item'),
        Rule(LinkExtractor(allow=('item/\d+', ),
                           restrict_xpaths=('//div[@class="alert prodLists"]/ul/li[@class="viewPics"]/p[@class="p-title"]/a[@target]', ),
                           deny=('pvp', 'pvl')), callback='parse_item'),
    )


    def parse_category(self, response):
        items = response.xpath(self.item_list_xpath)
        for item in items:
            link = item.extract()
            yield link


    def parse_item(self, response):

        loader = ProductLoader(item=ProductItem(), response=response)


        description = ''
        for row in response.xpath(self.desc_table_list_xpath):
            if row:
                name = row.xpath('td[1]//text()').extract()
                value = row.xpath('td[2]//text()').extract()
                name = ''.join(name)
                value = ''.join(value)
                description += name + ' ' + value + '\n'

        for field, xpath in self.item_fields.iteritems():
            loader.add_xpath(field, xpath)
        loader.add_value('description', description)
        yield loader.load_item()
        #loader.add_xpath('url', 'a/@href')
        #loader.add_value('category_id', 0)
        #yield loader.load_item()


import re

from scrapy import Request
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.linkextractors import LinkExtractor
from tutorialScrapy.items import ProductItem, CategoryItem
from scrapy.conf import settings
import re


class ProductLoader(ItemLoader):
    #default_output_processor = TakeFirst()
    title_out = TakeFirst()
    cost_usd_out = TakeFirst()
    item_code_out = TakeFirst()
    sku_out = TakeFirst()
    status = TakeFirst()
    category = TakeFirst()
    description = TakeFirst()


class ProductSpider(CrawlSpider):
    category_name = settings['CATEGORY_NAME']
    category_id = settings['CATEGORY_ID']

    def __init__(self, category_name=None, category_id=None, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.category_name = category_name
        self.category_id = category_id

    name = "product"
    allowed_domains = ["buyincoins.ru"]
    start_urls = [
        "http://www.buyincoins.ru/sitemap.html",
    ]

    category_list_xpath = '//div[@class="sitemap_line"]/a[@class="sitemap_title"]/following-sibling::div[@class="sitemap_category"]/a'
    item_list_xpath = '//li[@class="viewPics"]/p[@class="p-title"]/a[@target]/@href'
    #deals_list_xpath = '//li[@class="viewPics"]'
    media_list_xpath = '//div[@class="desc product_clear"]'
    desc_table_list_xpath = '//div[@class="desc product_clear"]//table/tbody/tr'
    main_images_list_xpath = '//div[@class="img l"]//img/@data-zoom-image'
    desc_images_list_xpath = '//div[@class="desc product_clear"]//img/@src'

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
        Rule(LinkExtractor(allow=('item/39671', ),
                           restrict_xpaths=('//div[@class="alert prodLists"]/ul/li[@class="viewPics"]/p[@class="p-title"]/a[@target]', ),
                           deny=('pvp', 'pvl')), callback='parse_item'),
    )

    def parse_category(self, response):
        items = response.xpath(self.item_list_xpath)
        for item in items:
            link = item.extract()
            yield link

    def parse_item(self, response):

        loader = ItemLoader(item=ProductItem(), response=response)

        description = ''
        for row in response.xpath(self.desc_table_list_xpath):
            if row:
                name = row.xpath('td[1]//text()').extract()
                value = row.xpath('td[2]//text()').extract()
                name = ''.join(name)
                value = ''.join(value)
                description += name + ' ' + value + '\n'

        #for field, xpath in self.item_fields.iteritems():
            #loader.add_xpath(field, xpath)

        #loader.add_value('description', description)

        images = response.xpath(self.main_images_list_xpath).extract()
        images.extend(response.xpath(self.desc_images_list_xpath).extract())

        product_item = ProductItem()
        product_item['title'] = response.xpath(self.item_fields['title']).extract()[0]
        product_item['cost_usd'] = re.findall("\d+\.\d+", response.xpath(self.item_fields['cost_usd']).extract()[0])
        product_item['item_code'] = response.xpath(self.item_fields['item_code']).extract()[0][12:]
        product_item['sku'] = response.xpath(self.item_fields['sku']).extract()[0]
        product_item['status'] = response.xpath(self.item_fields['status']).extract()[0]
        product_item['category'] = response.xpath(self.item_fields['category']).extract()[0]
        product_item['url'] = response.request.url
        product_item['description'] = description
        product_item['image_urls'] = images

        #loader.add_value('image_urls', images)

        #yield loader.load_item()
        yield product_item


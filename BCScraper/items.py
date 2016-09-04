# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst


class CategoryItem(Item):
    title = Field()
    url = Field()
    main_category = Field()
    category_id = Field(default=0)


class ProductItem(Item):
    title = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    cost_usd = Field(output_processor=TakeFirst())
    item_code = Field(output_processor=TakeFirst())
    sku = Field(output_processor=TakeFirst())
    status = Field(output_processor=TakeFirst())
    category = Field(output_processor=TakeFirst())
    description = Field(output_processor=TakeFirst())
    image_urls = Field()
    images = Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CategoryItem(Item):
    title = Field()
    url = Field()
    category_id = Field(default=0)


class ProductItem(Item):
    title = Field()
    cost_usd = Field()
    item_code = Field()
    sku = Field()
    status = Field()
    category = Field()
    description = Field()


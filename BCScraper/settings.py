# -*- coding: utf-8 -*-

# Scrapy settings for BCScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'BCScraper'

SPIDER_MODULES = ['BCScraper.spiders']
NEWSPIDER_MODULE = 'BCScraper.spiders'
DEFAULT_ITEM_CLASS = 'BCScraper.items.ProductItem'
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    #'BCScraper.pipelines.JsonExportPipeline': 400,
    'BCScraper.pipelines.MySQLStoreProductPipeline': 400
}

DATABASE_NAME = 'scrapy'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
TABLE_NAME = 'category'

CATEGORY_ID = 0
CATEGORY_NAME = 'Tablets-eReaders_356'
OUT_FILE = 'scraped_items.json'
IMAGES_STORE = 'd:/Pyton/MyBlog/blog/static/blog/images/'


#FEED_URI = 'scraped_items.json'
FEED_FORMAT = 'json'
#FEED_EXPORTERS = {
#    'json': 'scrapy.exporters.JsonLinesItemExporter'
#}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'BCScraper (+http://www.yourdomain.com)'

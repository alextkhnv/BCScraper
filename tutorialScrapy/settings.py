# -*- coding: utf-8 -*-

# Scrapy settings for tutorialScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tutorialScrapy'

SPIDER_MODULES = ['tutorialScrapy.spiders']
NEWSPIDER_MODULE = 'tutorialScrapy.spiders'
DEFAULT_ITEM_CLASS = 'tutorialScrapy.items.ProductItem'
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    #'tutorialScrapy.pipelines.JsonExportPipeline': 400,
    'tutorialScrapy.pipelines.MySQLStoreProductPipeline': 400
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
#USER_AGENT = 'tutorialScrapy (+http://www.yourdomain.com)'

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
#ITEM_PIPELINES = {
    #'tutorialScrapy.pipelines.JSONPipeline': 300,
#    'tutorialScrapy.pipelines.MySQLStorePipeline': 300,
#}

DATABASE_NAME = 'scrapy'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
TABLE_NAME = 'category'

CATEGORY_ID = 0
CATEGORY_NAME = 'Tablets-eReaders_356'


#FEED_URI = 'items.json'
#FEED_FORMAT = 'json'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorialScrapy (+http://www.yourdomain.com)'

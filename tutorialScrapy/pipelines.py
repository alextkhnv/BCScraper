# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import time
import unicodedata
import MySQLdb.cursors
from scrapy.conf import settings
from subprocess import Popen, PIPE

from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JsonExportPipeline(object):

    def __init__(self, out_file):
        self.out_file = out_file
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        out_file = settings.get("OUT_FILE")
        return cls(out_file)

    def spider_opened(self, spider):
        file = open(self.out_file, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MySQLStorePipeline(object):

    def __init__(self):
        # @@@ hardcoded db settings
        # TODO: make settings configurable through settings
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            db=settings['DATABASE_NAME'],
            user=settings['DATABASE_USER'],
            passwd=settings['DATABASE_PASSWORD'],
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=True
        )

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._insert, item)
        query.addErrback(self.handle_error)

        return item

    def _insert(self, tx, item):
        tx.execute("INSERT IGNORE INTO `" + settings['TABLE_NAME'] + "`\
                        (title, url, category_id)\
                    VALUES (%s, %s, %s)",
            (item['title'],
             item['url'],
             item['category_id'])
        )

    def handle_error(self, e):
        logging.error(e)


class MySQLStoreProductPipeline(MySQLStorePipeline):

    def _insert(self, tx, item):
        tx.execute("INSERT IGNORE INTO `Product`\
                        (title, cost_usd, item_code, sku, category, description, url, images, status)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (item['title'],
             item['cost_usd'],
             item['item_code'],
             item['sku'],
             item['category'],
             item['description'],
             item['url'],
             json.dumps(item['images']),
             item['status'])
        )



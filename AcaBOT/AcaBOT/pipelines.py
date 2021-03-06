# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import pymongo

#from scrapy.conf import settings


#class MongoDBPipeline(object):

#    def __init__(self):
#        connection = pymongo.MongoClient(
#            settings['MONGODB_SERVER'],
#            settings['MONGODB_PORT']
#        )
#        db = connection[settings['MONGODB_DB']]
#        self.collection = db[settings['MONGODB_COLLECTION']]

#    def process_item(self, item, spider):
#        for data in item:
#            if not data:
#                raise DropItem("Missing data!")
#        self.collection.insert(dict(item))

#        return item

#import pymongo

#class MongoPipeline(object):

#    collection_name = 'scrapy_items'

#    def __init__(self, mongo_uri, mongo_db):
#        self.mongo_uri = mongo_uri
#        self.mongo_db = mongo_db

#    @classmethod
#    def from_crawler(cls, crawler):
#        return cls(
#            mongo_uri=crawler.settings.get('MONGO_URI'),
#            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#        )

#    def open_spider(self, spider):
#        self.client = pymongo.MongoClient(self.mongo_uri)
#        self.db = self.client[self.mongo_db]

#    def close_spider(self, spider):
#        self.client.close()

#    def process_item(self, item, spider):
#        self.db[self.collection_name].insert_one(dict(item))
#        return item

import pymongo
import gridfs
import mimetypes
import requests

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.grid_fs = gridfs.GridFS(getattr(connection, settings['MONGODB_DB']))

    def process_item(self, item, spider):
        links = item['image_urls']
        ids = []
        for i, link in enumerate(links):
            mime_type = mimetypes.guess_type(link)[0]
            request = requests.get(link, stream=True)
            _id = self.grid_fs.put(request.raw, contentType=mime_type, filename=item['images'][i])
            ids.append(_id)
        self.collection.insert(dict(item))

        return item
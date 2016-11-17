# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings



class MongoDBPipeline(object):
    collection_name = 'zhihu_users'

    # def __init__(self, mongo_uri, mongo_db):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db


    # @classmethod
    # def from_crawler(class_, crawler):
    #     pass
    
    # def open_spider(self, spider):
    #     self.client = pymongo.MongoClient(self.mongo_uri)
    #     self.db = self.client[self.mongo_db]

    # def close_spider(self, spider):
    #     self.client.close()


    # def process_item(self, item, spider):
    #     self.db[self.collection_name].insert_one(item)
    #     return item
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

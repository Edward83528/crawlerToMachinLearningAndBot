# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
import codecs

class PttPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
 
    def __init__(self):
        pass
 
    def process_item(self, item, spider):
        json_file_name = dict(item)['board']
        self.file = codecs.open(json_file_name+'.json', 'a', encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
 
    def spider_closed(self, spider):
        self.file.close()

class MongoPipeline(object):
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = dict(item)['board']
        #self.db[collection_name].insert(dict(item))
        try:
            try:
                index_name = 'date_-1'
                if index_name not in self.db[collection_name].index_information():
                    self.db[collection_name].create_index([('date', pymongo.DESCENDING)])
            except Exception as e:
                pass
            try:
                index_name = 'url_-1'
                if index_name not in self.db[collection_name].index_information():
                    self.db[collection_name].create_index([('url', pymongo.DESCENDING)])
            except Exception as e:
                pass
            key = {"url" : dict(item)['url']}
            self.db[collection_name].update(key,dict(item),True)
        except Exception as e:
            self.db[collection_name].create_index([('url', pymongo.DESCENDING), ('date', pymongo.DESCENDING)])
            self.db[collection_name].insert(dict(item))
        return item

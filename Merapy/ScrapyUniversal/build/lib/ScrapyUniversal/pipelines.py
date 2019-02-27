# -*- coding: utf-8 -*-

import pymongo
from random import choice
from ScrapyUniversal.custom_settings import COLLECTION, ITEM


class ScrapyuniversalPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, download_path):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.download_path = download_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('ALICE_MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            download_path=crawler.settings.get('DOWNLOAD_PATH'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        key_items = dict(item)
        r_key = choice(list(item))
        for i in range(len(key_items[r_key])):
            new_items = {}
            for key, items in key_items.items():
                # new_items.setdefault(key, items[i])
                try:
                    new_items.setdefault(key, items[i])
                except:
                    new_items.setdefault(key, u'该页有数据缺失')
            self.db[COLLECTION].insert(new_items)
        # self.db[COLLECTION].insert(dict(item))
        return item

    def close_spider(self, spider):
        data = self.db[COLLECTION].find(projection={'_id': False})
        key = self.db[COLLECTION].find(projection={'_id': False}).limit(1).next()
        self.client.close()
        with open(self.download_path, 'w', encoding='UTF-8') as f:
            for i in key:
                f.write(i + '\t')
            f.write('\n')
            for item in data:
                for key in item:
                    f.write(item[key] + '\t')
                f.write('\n')
            f.close()


class CloudDownLoad(object):
    def __init__(self, download_path):
        self.download_path = download_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            download_path=crawler.settings.get('DOWNLOAD_PATH'),
        )

    def process_item(self, item, spider):
        key_items = dict(item)
        r_key = choice(list(item))
        with open(self.download_path, 'a', encoding='UTF-8') as f:
            for i in range(len(key_items[r_key])):
                new_items = {}
                for key, items in key_items.items():
                    # new_items.setdefault(key, items[i])
                    try:
                        new_items.setdefault(key, items[i])
                    except:
                        new_items.setdefault(key, u'该页有数据缺失')
                    f.write(items[i] + '\t')
                f.write('\n')
            f.close()
        return item

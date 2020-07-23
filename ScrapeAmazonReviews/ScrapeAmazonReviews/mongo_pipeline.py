import pymongo
from itemadapter import ItemAdapter


class MongoPipeline:

    collection_name = 'products'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb+srv://tracksentiments2020:track2020@cluster0.yse0l.mongodb.net/tracksentiments?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE',
            mongo_db='tracksentiments'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        cursor = self.db[self.collection_name].find({"_id": item['_id']})
        if cursor.count() == 0:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        else:
            self.db[self.collection_name].update_one({ "_id": item['_id'] }, {"$set": ItemAdapter(item).asdict()})
        return item
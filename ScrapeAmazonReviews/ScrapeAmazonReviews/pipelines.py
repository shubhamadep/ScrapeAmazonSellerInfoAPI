# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class ScrapeamazonreviewsPipeline(object):
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('product_price'):
            return item
        else:
            raise DropItem("Missing price in %s" % item)
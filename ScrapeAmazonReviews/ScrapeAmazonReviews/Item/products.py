# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeAmazonProduct(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # name = scrapy.Field()
    product_title = scrapy.Field()
    product_price = scrapy.Field()
    product_image_link = scrapy.Field()
    product_link = scrapy.Field()
    asin = scrapy.Field()
    product_reviews_url = scrapy.Field()
    seller_name = scrapy.Field()
    product_count = scrapy.Field()
    
    pass

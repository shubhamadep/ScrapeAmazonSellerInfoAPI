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
    productTitle = scrapy.Field()
    productPrices = scrapy.Field()
    productImageLink = scrapy.Field()
    productLink = scrapy.Field()
    asin = scrapy.Field()
    productreviewsurl = scrapy.Field()
    pass

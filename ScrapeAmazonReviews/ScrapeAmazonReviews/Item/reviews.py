import scrapy


class ScrapeAmazonReviews(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # name = scrapy.Field()
    customer_name = scrapy.Field()
    ratings = scrapy.Field()
    review_title = scrapy.Field()
    reviews = scrapy.Field()
    timestamp = scrapy.Field()
    pass

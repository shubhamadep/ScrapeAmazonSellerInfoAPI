REDIS_URL = "redis://redistogo:20f95cdac0872696029dfe1396df2f08@pike.redistogo.com:11374/"
MONGO_DB_URI = "mongodb+srv://tracksentiments2020:track2020@cluster0.yse0l.mongodb.net/tracksentiments?retryWrites=true&w=majority"
MONGO_DB_DATABASE = 'tracksentiments'

from scrapy.crawler import CrawlerProcess
CRAWL_RUNNER = CrawlerProcess({
   'ROBOTSTXT_OBEY': True,
   'ROTATING_PROXY_LIST_PATH': './proxies.txt',
   'DOWNLOADER_MIDDLEWARES': {
       'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
       'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
       'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
       'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
   },
   'ITEM_PIPELINES' : {
    'ScrapeAmazonReviews.ScrapeAmazonReviews.mongo_pipeline.MongoPipeline': 400
}

   })
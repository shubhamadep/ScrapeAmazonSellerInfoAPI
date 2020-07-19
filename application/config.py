REDIS_URL = "redis://redistogo:20f95cdac0872696029dfe1396df2f08@pike.redistogo.com:11374/"
MONGO_DB_URI = "mongodb://kamlesh:kamlesh123@ds035703.mlab.com:35703/heroku_6zrt4zs1"
MONGO_DB_DATABASE = 'heroku_6zrt4zs1'

from scrapy.crawler import CrawlerProcess
CRAWL_RUNNER = CrawlerProcess({
   'ROBOTSTXT_OBEY': True,
   'ROTATING_PROXY_LIST_PATH': './proxies.txt',
   'DOWNLOADER_MIDDLEWARES': {
       'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
       'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
       'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
       'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
   }})
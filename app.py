import crochet
crochet.setup()

import flask
from flask import request
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings

from ScrapeAmazonReviews.ScrapeAmazonReviews.spiders import AmazonSpider


crawl_runner = CrawlerProcess({
   'ROBOTSTXT_OBEY': True,
   'ROTATING_PROXY_LIST_PATH': './proxies.txt',
   'DOWNLOADER_MIDDLEWARES': {
       'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
       'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
       'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
       'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
   }})

output_data = []
app = flask.Flask(__name__)

@crochet.wait_for(timeout=60.0)
def scrape_amazon_reviews(sellerID):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(AmazonSpider.AmazonspiderSpider, url=sellerID)
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))

def formatting_reviews(reviews):
    corpus = []
    for paginatedReviews in reviews:
        for review in paginatedReviews['productInfo']:
            if review != '\n            ':
                corpus.append(review)
    return corpus

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route("/scrape", methods=["GET", "POST"])
def predict():
    
    args = request.args
    sellerID = args["SellerID"]
    print ("SELLER ID: ", args["SellerID"])

    data = {"success": False}

    scrape_amazon_reviews(sellerID)
    formatted_output = formatting_reviews(output_data)
    print("output: ",formatted_output)

    # if not formatted_output:
    data["ProductInfo"] = formatted_output
    data = {"success": True}
    
    response = flask.jsonify(data)

    return response

if __name__ == "__main__":
    '''
        use 
            app.run(host='0.0.0.0', port=5500) to run locally. 
        
        Threaded option to enable multiple instances for multiple user access support
            app.run(threaded=True, port=5000)
    '''
    # app.run(host='0.0.0.0', port=5500)
    app.run(threaded=True, port=5000)
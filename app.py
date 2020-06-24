import crochet
crochet.setup()

import flask
from flask import request
from flask_redis import FlaskRedis
import json
import config as cfg
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from ScrapeAmazonReviews.ScrapeAmazonReviews.spiders import ProductReviewSpider
from ScrapeAmazonReviews.ScrapeAmazonReviews.spiders import AmazonSpider
from ScrapeAmazonReviews.ScrapeAmazonReviews.helpers.format import formatting_response_list, formatting_response_dict

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
review_details = []
app = flask.Flask(__name__)
app.config['REDIS_URL'] = cfg.REDIS_URL
redis_client = FlaskRedis(app)
output = {}

def check_redis_for_response(key):

    if redis_client.exists(key): return True
    return False

@crochet.wait_for(timeout=60.0)
def scrape_amazon_products(sellerID):
    
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(AmazonSpider.AmazonspiderSpider, url=sellerID)
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))

@crochet.wait_for(timeout=240.0)
def scrape_product_reviews(asin):
    dispatcher.connect(review_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(ProductReviewSpider.ProductReviewSpider, parameters=asin)
    return eventual

def review_crawler_result(item, response, spider):
    review_details.append(dict(item))

@app.route('/')
def index():
    return "<h1>Welcome to our API, lets scrape..</h1>"

@app.route("/getproductdetails/scrape", methods=["GET"])
def get_product_details():

    args = request.args
    sellerID = args["SellerID"]
    print ("SELLER ID: ", args["SellerID"])
    
    data = {"success": False}

    if check_redis_for_response(sellerID):
        return json.loads(redis_client.get(sellerID))

    scrape_amazon_products(sellerID)

    formatted_product_info = output_data[0]['productTitle']
    formatted_price_info = output_data[0]['productPrices']
    formatted_product_image_link = output_data[0]['productImageLink']
    formatted_product_link = output_data[0]['productLink']
    formatted_product_reviews_url = output_data[0]['productreviewsurl']
    formatted_asin = output_data[0]['asin']

    # if not formatted_output:
    d = {}

    d["productTitle"] = formatted_product_info
    d["ProductPrices"] = formatted_price_info
    d["ProductImageLink"] = formatted_product_image_link
    d["ProductLink"] = formatted_product_link
    d["ASIN"] = formatted_asin
    d["ProductReviewsUrl"] = formatted_product_reviews_url

    
    output = formatting_response_dict(d, len(formatted_product_info))
    
    data = {"success": True,
            "items" : output
            }
    
    response = flask.jsonify(data)
    redis_client.set(sellerID, json.dumps(data))
    return response

@app.route("/reviews/scrape", methods=["GET"])
def get_product_reviews():
    
    args = request.args
    asin = args["ASIN"]
    print ("ASIN : ", args["ASIN"])
    
    data = {"success": False}

    if check_redis_for_response(asin):
        return json.loads(redis_client.get(asin))

    scrape_product_reviews(asin)


    formatted_reviews = [y for x in [review_details[index]['reviews'] for index in range(0,len(review_details))] for y in x]
    formatted_ratings = [y for x in [review_details[index]['ratings'] for index in range(0,len(review_details))] for y in x]
    formatted_review_title = [y for x in [review_details[index]['review_title'] for index in range(0,len(review_details))] for y in x]
    formatted_timestamp = [y for x in [review_details[index]['timestamp']for index in range(0,len(review_details))] for y in x]
    formatted_customer_name = [y for x in [review_details[index]['customer_name']for index in range(0,len(review_details))] for y in x]
    d = {}

    d["Rating"] = formatted_ratings
    d["Title"] = formatted_review_title
    d["Review"] = formatted_reviews
    d["Date"] = formatted_timestamp
    d["CustomerName"] = formatted_customer_name
    
    output = formatting_response_list(d, len(formatted_review_title))

    data = {"success": True,
            "items": output
            }
    
    response = flask.jsonify(data)
    redis_client.set(asin, json.dumps(data))

    return response

if __name__ == "__main__":
    '''
        use 
            app.run(host='0.0.0.0', port=5500) to run locally. 
        
        Threaded option to enable multiple instances for multiple user access support
            app.run(threaded=True, port=5000)
    '''
    # app.run(host='0.0.0.0', port=5500)
    app.run(threaded=True, port=5000, debug=True)
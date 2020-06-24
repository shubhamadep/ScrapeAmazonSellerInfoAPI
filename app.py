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
from ScrapeAmazonReviews.ScrapeAmazonReviews.helpers.format import format_response_list, format_response_dict, format_scrapped_data
#MongoDB imports


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

    formatted_product_info = format_scrapped_data(output_data,'productTitle')
    formatted_price_info = format_scrapped_data(output_data,'productPrices')
    formatted_product_image_link = format_scrapped_data(output_data,'productImageLink')
    formatted_product_link = format_scrapped_data(output_data,'productLink')
    formatted_product_reviews_url = format_scrapped_data(output_data,'productreviewsurl')
    formatted_asin = format_scrapped_data(output_data,'asin')

    # if not formatted_output:
    d = {}

    d["productTitle"] = formatted_product_info
    d["ProductPrices"] = formatted_price_info
    d["ProductImageLink"] = formatted_product_image_link
    d["ProductLink"] = formatted_product_link
    d["ASIN"] = formatted_asin
    d["ProductReviewsUrl"] = formatted_product_reviews_url

    
    output = format_response_dict(d, len(formatted_product_info))
    
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


    formatted_reviews = format_scrapped_data(review_details,'reviews')
    formatted_ratings = format_scrapped_data(review_details,'ratings')
    formatted_review_title = format_scrapped_data(review_details,'review_title')
    formatted_timestamp = format_scrapped_data(review_details,'timestamp')
    formatted_customer_name = format_scrapped_data(review_details,'customer_name')

    d = {}

    d["Rating"] = formatted_ratings
    d["Title"] = formatted_review_title
    d["Review"] = formatted_reviews
    d["Date"] = formatted_timestamp
    d["CustomerName"] = formatted_customer_name
    
    output = format_response_list(d, len(formatted_review_title))

    data = {"success": True,
            "items": output
            }
    
    response = flask.jsonify(data)
    redis_client.set(asin, json.dumps(data))

    return response


"""MongoDB Server Instance Testing"""

@app.route("/mongoDBTest/all", methods=["GET"])
def getAllProductInfo():
    testProduct = productInfo.productInfo.query.all()
    dictn  = {}
    for x in testProduct:
        dictn['testDocument'] = x.testDocument
    response = flask.jsonify(dictn)
    return response

if __name__ == "__main__":
    '''
        use 
            app.run(host='0.0.0.0', port=5500) to run locally. 
        
        Threaded option to enable multiple instances for multiple user access support
            app.run(threaded=True, port=5000)
    '''

    # app.run(host='0.0.0.0', port=5500)
    from databaseConfig import db
    import  model.productInfo as productInfo
    app.run(threaded=True, port=5000, debug=True)
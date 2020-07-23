import crochet
crochet.setup()
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from ScrapeAmazonReviews.ScrapeAmazonReviews.spiders import AmazonSpider
from ScrapeAmazonReviews.ScrapeAmazonReviews.helpers.format import format_response_list, format_response_dict, format_scrapped_data
from flask_redis import FlaskRedis
import flask
import json
from flask import request, Blueprint
from application.config import CRAWL_RUNNER
from application.databaseConfig import db
output_data = []
output = {}

getproducts = Blueprint('getproducts',__name__)

@crochet.wait_for(timeout=240.0)
def scrape_amazon_products(sellerID):

    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = CRAWL_RUNNER.crawl(AmazonSpider.AmazonspiderSpider, url=sellerID)
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))

def check_redis_for_response(key, redis_client):
    if redis_client.exists(key): return True
    return False

@getproducts.route("/getproductdetails/scrape", methods=["GET"])
def get_product_details():
    from app import redis_client
    args = request.args
    sellerID = args["SellerID"]
    print ("SELLER ID: ", args["SellerID"])
    
    data = {"success": False}

    if check_redis_for_response(sellerID, redis_client):
        return json.loads(redis_client.get(sellerID))

    scrape_amazon_products(sellerID)
    output_data = []
    output_data = db['products'].find({"_id": sellerID})
    output_data = list(output_data)[0]
    print('output_data', output_data)
    if output_data!=[]:
        formatted_product_info = format_scrapped_data(output_data,'product_title')
        formatted_price_info = format_scrapped_data(output_data,'product_price')
        formatted_product_image_link = format_scrapped_data(output_data,'product_image_link')
        formatted_product_link = format_scrapped_data(output_data,'product_link')
        formatted_product_reviews_url = format_scrapped_data(output_data,'product_reviews_url')
        formatted_asin = format_scrapped_data(output_data,'asin')

        d = {}

        d["productTitle"] = formatted_product_info
        d["ProductPrices"] = formatted_price_info
        d["ProductImageLink"] = formatted_product_image_link
        d["ProductLink"] = formatted_product_link
        d["ASIN"] = formatted_asin
        d["ProductReviewsUrl"] = formatted_product_reviews_url

        print('length',len(d["productTitle"]),len(d["ProductPrices"]),len(d["ProductImageLink"]),len(d["ProductLink"])
        ,len(d["ProductReviewsUrl"]),len(d["ASIN"]))
        output = format_response_dict(d, len(formatted_product_info))
    
        data = {"success" : True,
                "sellerName" : output_data['seller_name'][0],
                "product_count" : len(d["ASIN"]),
                "seller_rating" : output_data['seller_ratings'],
                "seller_review" : output_data['seller_reviews'],
                "items" : output
                }
    
        response = flask.jsonify(data)
        #redis_client.set(sellerID, json.dumps(data),86400)
        return response
    else:
        return ('<h1>There was a problem scraping product details</h1>')

import crochet
crochet.setup()

from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from flask_redis import FlaskRedis
from ScrapeAmazonReviews.ScrapeAmazonReviews.spiders import ProductReviewSpider
from ScrapeAmazonReviews.ScrapeAmazonReviews.helpers.format import format_response_list, format_response_dict, format_scrapped_data
import flask

import json
from flask import request, Blueprint
from scrapy import signals
from application.config import CRAWL_RUNNER

review_details = []

getreviews = Blueprint('getreviews',__name__)

@crochet.wait_for(timeout=240.0)
def scrape_product_reviews(asin):
    dispatcher.connect(review_crawler_result, signal=signals.item_scraped)
    eventual = CRAWL_RUNNER.crawl(ProductReviewSpider.ProductReviewSpider, parameters=asin)
    return eventual

def review_crawler_result(item, response, spider):
    review_details.append(dict(item))

def check_redis_for_response(key, redis_client):
    if redis_client.exists(key): return True
    return False

@getreviews.route("/reviews/scrape", methods=["GET"])
def get_product_reviews():
    from app import redis_client
    args = request.args
    asin = args["ASIN"]
    print ("ASIN : ", args["ASIN"])
    
    data = {"success": False}

    if check_redis_for_response(asin, redis_client):
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
    redis_client.set(asin, json.dumps(data),86400)

    return response
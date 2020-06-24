# -*- coding: utf-8 -*-
import scrapy
from ..Item.reviews import ScrapeAmazonReviews
from urllib.parse import urljoin
from datetime import datetime

class ProductReviewSpider(scrapy.Spider):

    def __init__(self, parameters=None, *args, **kwargs):
        
        
        # url as a parameter receives SellerID.
        
        self.product_review_url = parameters
        self.start_urls = [
            'https://www.amazon.com/s?k='+parameters+'&ref=nb_sb_noss'
            ]
        self.name = 'ProductReviewSpider' 

    def parse(self, response):

        product_url = response.xpath('.//h2[contains(@class, "a-size-mini a-spacing-none a-color-base s-line-clamp-2")]').xpath('.//a[contains(@class, "a-link-normal a-text-normal")]/@href').extract()
        product_title = product_url[0].split('/dp/')[0][1:]
        product_reviews_url = 'https://www.amazon.com/'+product_title+'/product-reviews/'+self.product_review_url+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
        print('Product Reviews URL : ',product_reviews_url)

        yield scrapy.Request(product_reviews_url, callback=self.parse_reviews)
    
    def parse_reviews(self, response):
        items = ScrapeAmazonReviews()
        review_title = response.css('.a-text-bold span').css('::text').extract()
        ratings = response.xpath('.//a[contains(@class, "a-link-normal")]').xpath('.//i[contains(@data-hook, "review-star-rating")]').xpath('.//span[contains(@class,"a-icon-alt")]//text()').extract()

        reviews = response.xpath('.//span[contains(@data-hook, "review-body")]/span [descendant-or-self::text()]').extract()
        reviews = [review.replace('<span>','').replace('</span>','').replace('<br>','') for review in reviews]

        timestamp = response.css('#cm_cr-review_list .review-date').css('::text').extract()
        timestamp = [ts.split(' on ')[1] for ts in timestamp]
        
        items['reviews'] = reviews
        items['ratings'] = [rating.split(' out')[0] for rating in ratings]
        items['review_title'] = review_title
        items['timestamp'] = timestamp

        

        next_page_url = response.xpath('.//li[contains(@class, "a-last")]/a/@href').get()
        absolute_next_page_url = response.urljoin(next_page_url)

        yield items
        yield scrapy.Request(absolute_next_page_url, callback=self.parse_reviews)
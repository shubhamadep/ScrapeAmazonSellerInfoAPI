# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapeamazonreviewsItem

class AmazonspiderSpider(scrapy.Spider):

    def __init__(self, url=None, *args, **kwargs):
        
        '''
            url as a parameter receives SellerID.
        '''

        self.Amazon_Standard_Identification_Number = url
        print("Parsing Seller ID: ", self.Amazon_Standard_Identification_Number)
        self.page_number = 1
        # self.start_urls = ['https://www.amazon.com/Echo-Wall-Clock-requires-compatible/product-reviews/'+self.Amazon_Standard_Identification_Number+'/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(1)]
        self.start_urls = ['https://www.amazon.com/s?me='+str(self.Amazon_Standard_Identification_Number)+'&marketplaceID=ATVPDKIKX0DER']
        self.name = 'AmazonSpider'


    def parse(self, response):
        print('parser is called.')
        items = ScrapeamazonreviewsItem()
        print("item: ", ScrapeamazonreviewsItem)
        productInfo = response.css('.a-text-normal span::text').extract()
        productPrices = response.css('.a-price-whole span::text').extract()

        items['productInfo'] = productInfo
        items['productPrices'] = productPrices
        #
        yield items

        # next_page = 'https://www.amazon.com/Echo-Wall-Clock-requires-compatible/product-reviews/'+self.Amazon_Standard_Identification_Number+'/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(self.page_number)
        # if self.page_number <= 3:
        #     self.page_number += 1
        #     yield response.follow(next_page, callback = self.parse)

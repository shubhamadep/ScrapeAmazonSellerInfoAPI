# -*- coding: utf-8 -*-
import scrapy
from ..Item.products import ScrapeAmazonProduct
from urllib.parse import urljoin

class AmazonspiderSpider(scrapy.Spider):

    def __init__(self, url=None, *args, **kwargs):     
        # url as a parameter receives SellerID.      
        self.Amazon_Standard_Identification_Number = url
        print("Parsing Seller ID: ", self.Amazon_Standard_Identification_Number)
        self.page_number = 1
        self.start_urls = [
            'https://www.amazon.com/s?me='+str(self.Amazon_Standard_Identification_Number)+'&marketplaceID=ATVPDKIKX0DER'
            ]
        self.name = 'AmazonSpider' 
        self.seller_name = ''
        self.product_count = 0


    def parse(self, response):
        print('parser is called.')
        return scrapy.Request(self.start_urls[0], callback=self.parse_product_page)


    def parse_product_page(self, response):
        items = ScrapeAmazonProduct()
        product_title = response.css('.a-size-medium').css('::text').extract()
        product_price = response.xpath('.//span[contains(@class,"a-price")][contains(@data-a-color,"base")]//span[contains(@class,"a-offscreen")]//text()').extract()
        product_image_link = response.css('.s-image-fixed-height .s-image').css('::attr(src)').extract()
        product_link = response.xpath('.//h2[contains(@class, "a-size-mini a-spacing-none a-color-base s-line-clamp-2")]').xpath('.//a[contains(@class, "a-link-normal a-text-normal")]/@href').extract()
        

        next_page_url = response.xpath('.//li[contains(@class, "a-last")]/a/@href').get()
        absolute_next_page_url = response.urljoin(next_page_url)

        items['product_title'] = product_title
        items['product_price'] = product_price
        items['product_image_link'] = product_image_link
        items['product_link'] = product_link

        if self.seller_name == '':
            self.seller_name = response.css('.a-color-state').css('::text').extract()
            items['seller_name'] = self.seller_name
            
        if self.product_count == 0:
            self.product_count = response.css('.sg-col-30-of-36 span:nth-child(1)').css('::text').extract()
            pc = self.product_count[0].split('results')
            count = pc[0].split()
            print('count', count)
            if len(count) == 1:
                items['product_count'] = count[0]
            else:
                items['product_count'] = count[2]
        asin = []
        product_reviews_url = []

        for i in range(0,len(product_link)):
            product_link[i] = response.urljoin(product_link[i])
            productSplit = product_link[i].split("/dp/")
            asin.append(productSplit[1].split("/")[0])
            product_reviews_url.append(productSplit[0]+'/product-reviews/'+asin[i]+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
            
            
        items['asin'] = asin
        items['product_reviews_url'] = product_reviews_url
        
        yield items 
        yield scrapy.Request(absolute_next_page_url, callback=self.parse_product_page)
        
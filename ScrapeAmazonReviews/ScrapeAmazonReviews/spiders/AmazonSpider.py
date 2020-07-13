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
        self.sellerName = ''

    def parse(self, response):
        print('parser is called.')
        return scrapy.Request(self.start_urls[0], callback=self.parse_product_page)


    def parse_product_page(self, response):
        items = ScrapeAmazonProduct()
        productInfo = response.css('.a-size-medium').css('::text').extract()
        productPrices = response.xpath('.//span[contains(@class,"a-price")][contains(@data-a-color,"base")]//span[contains(@class,"a-offscreen")]//text()').extract()
        productImageLink = response.css('.s-image-fixed-height .s-image').css('::attr(src)').extract()
        productLink = response.xpath('.//h2[contains(@class, "a-size-mini a-spacing-none a-color-base s-line-clamp-2")]').xpath('.//a[contains(@class, "a-link-normal a-text-normal")]/@href').extract()
        

        next_page_url = response.xpath('.//li[contains(@class, "a-last")]/a/@href').get()
        absolute_next_page_url = response.urljoin(next_page_url)

        items['productTitle'] = productInfo
        items['productPrices'] = productPrices
        items['productImageLink'] = productImageLink
        items['productLink'] = productLink

        if self.sellerName == '':
            self.sellerName = response.css('.a-color-state').css('::text').extract()
            items['sellerName'] = self.sellerName
            print('sellerName :',items['sellerName'])
        
        asin = []
        productreviewsurl = []

        for i in range(0,len(productLink)):
            productLink[i] = response.urljoin(productLink[i])
            productSplit = productLink[i].split("/dp/")
            asin.append(productSplit[1].split("/")[0])
            productreviewsurl.append(productSplit[0]+'/product-reviews/'+asin[i]+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
            
            
        items['asin'] = asin
        items['productreviewsurl'] = productreviewsurl
        yield items

        yield scrapy.Request(absolute_next_page_url, callback=self.parse_product_page)
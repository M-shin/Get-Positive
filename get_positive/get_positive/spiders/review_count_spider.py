import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import ReviewCountItem
from datetime import datetime, timedelta
import os
from pymongo import MongoClient
import re
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

HOME = os.environ['HOME']
os.chdir(HOME + "/Desktop/github/hackathon/Get-Positive/get_positive/get_positive") 

class review_count_spider(CrawlSpider):
  name = 'review_count_spider'
  allowed_domains = ['yelp.com']

  def __init__(self, *args, **kwargs): 
    super(review_count_spider, self).__init__(*args, **kwargs) 
    self.start_urls = [kwargs.get('start_url')]

  def parse(self,response):

    if response.status < 600:
      # Get reviews/ratings on current page
      count = int(response.xpath('//span[@itemprop="reviewCount"]/text()').extract()[0])
      yield self.parse_count(count)

    else:
      time.sleep(10)
      yield scrapy.Request(response.url,callback=self.parse)

  # Parse page
  def parse_count(self, count):

    writer = open('reviewCounts.csv', 'wb')
    writer.write(str(count))
    writer.close()

    item = ReviewCountItem(
      count = count
    )
    return item

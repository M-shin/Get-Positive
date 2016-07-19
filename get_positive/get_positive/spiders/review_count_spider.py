import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from get_positive.get_positive.items import ReviewCountItem
from datetime import datetime, timedelta
from pymongo import MongoClient
import re
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class review_count_spider(CrawlSpider):
  name = 'review_count_spider'
  allowed_domains = ['yelp.com']

  def __init__(self, *args, **kwargs):
    super(review_count_spider, self).__init__(*args, **kwargs)
    self.start_urls = [kwargs.get('start_url')]

  def parse(self,response):

    if response.status < 600:
      # Get reviews/ratings on current page
      pretty_name = response.xpath('//h1[@class="biz-page-title embossed-text-white shortenough"]/text()').extract()[0].replace('\n', '').strip()
      count = int(response.xpath('//span[@itemprop="reviewCount"]/text()').extract()[0])
      yield self.parse_count(count, pretty_name)

    else:
      time.sleep(10)
      yield scrapy.Request(response.url,callback=self.parse)

  # Parse page
  def parse_count(self, count, pretty_name):

    writer = open('reviewCounts.csv', 'wb')
    writer.write(str(count) + ',' + pretty_name)
    writer.close()

    item = ReviewCountItem(
      count = count
    )
    return item

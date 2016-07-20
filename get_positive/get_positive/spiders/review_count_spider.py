import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import ReviewCountItem
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
      pretty_name = response.xpath('//h1[@class="biz-page-title embossed-text-white shortenough"]/text()').extract()[0].replace('\n', '').strip().encode('ascii', 'ignore')
      count = int(response.xpath('//span[@itemprop="reviewCount"]/text()').extract()[0])
      zip_code = response.xpath('//span[@itemprop="postalCode"]/text()').extract()[0]
      yield self.parse_count(count, pretty_name, zip_code)

    else:
      time.sleep(10)
      yield scrapy.Request(response.url,callback=self.parse)

  # Parse page
  def parse_count(self, count, pretty_name, zip_code):

    writer = open('get_positive/get_positive/reviewCounts.csv', 'wb')
    try:
      writer.write(str(count) + ',' + str(pretty_name) + ',' + str(zip_code))
    except UnicodeDecodeError:
      pass
    writer.close()

    item = ReviewCountItem(
      count = count
    )
    return item

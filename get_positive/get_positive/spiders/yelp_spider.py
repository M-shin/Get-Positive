import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import YelpItem
from datetime import datetime, timedelta
import os
import re
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

os.chdir('../get_positive') 

class yelp_spider(CrawlSpider):
  name = 'yelp_spider'
  allowed_domains = ['yelp.com']

  def __init__(self, *args, **kwargs): 
    super(yelp_spider, self).__init__(*args, **kwargs) 
    self.start_urls = [kwargs.get('start_url')]
    self.start_page = kwargs.get('page_num')
    self.page_num = kwargs.get('page_num')

    self.coll = kwargs.get('coll')

    if self.coll.count({'name': self.restaurant_name}) > 0:
      return

    self.coll.insert_one({
        'name': self.restaurant_name,
        'menuItems': [],
        'reviews': [],
        'url': self.start_urls[0].split('?start')[0]
      })

  def parse(self,response):

    if response.status < 600:
      # Get reviews/ratings on current page
      page_reviews = response.xpath('//div[@class="review-content"]/p[@itemprop="description"]').extract()
      ratings = response.xpath('//meta[@itemprop="ratingValue"]').extract()
     
      for i in range(len(page_reviews)):
        yield self.parse_review(page_reviews[i], ratings[i+1])

      # Paginate 5 pages
      if response.xpath('//span[@class="pagination-label responsive-hidden-small pagination-links_anchor"]') and (self.page_num - self.start_page) <= 100:
        self.page_num += 20
        base_url = self.start_urls[0].split('?start=')[0]
        yield scrapy.Request(base_url + '?start=' + str(self.page_num), callback=self.parse)

    else:
      time.sleep(10)
      yield scrapy.Request(response.url,callback=self.parse)

  # Parse page
  def parse_review(self, review, rating):
    clean_review = re.sub(r'<p itemprop="description".+?>', '', review.replace('</p>', ''))
    clean_rating = float(rating.split('content')[1][2:5])

    self.coll.update_one(
      {'name': self.restaurant_name},
      {'$push': {
          'reviews': {
            'body': clean_review,
            'rating': clean_rating
          }
        }
      }
    )

    item = YelpItem(
      body = clean_review,
      rating = clean_rating
    )
    return item

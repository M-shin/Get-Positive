import csv
import math

from scrapy import cmdline
from spiders.yelp_spider import yelp_spider
from spiders.review_count_spider import review_count_spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from datetime import datetime
from pymongo import MongoClient

# url = 'https://www.yelp.com/biz/fang-san-francisco-2'

def getReviewCount(url):
  # Get the number of reviews
  process = CrawlerProcess(get_project_settings())
  process.crawl(review_count_spider, start_url=url)

  with open("reviewCounts.csv", 'rU') as csvfile:
      reader = csv.reader(csvfile, delimiter = ',')
      for row in reader:
        return row[1]

import csv
import math

from scrapy import cmdline
from spiders.yelp_spider import yelp_spider
from spiders.review_count_spider import review_count_spider
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
from pymongo import MongoClient

# url = 'https://www.yelp.com/biz/fang-san-francisco-2'

def scrapeReviews(url):

  # Read in number of reviews
  numReviews = 0
  with open("reviewCounts.csv", 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
      numReviews = int(row[0])

  # Scrape/crawl restaurant on Yelp
  client = MongoClient()
  db = client['reviews_db']
  coll = db['reviews']
  process = CrawlerProcess(get_project_settings())
  process.crawl(yelp_spider, start_url=url, coll=coll)
  num = 0
  while num < numReviews:
    process.crawl(yelp_spider, start_url=(url + '?start=' + str(num)), coll=coll, page_num=num)
    num += 100

  process.start()

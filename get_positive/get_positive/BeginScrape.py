import argparse
import csv
import math

from scrapy import cmdline
from spiders.yelp_spider import yelp_spider
from spiders.review_count_spider import review_count_spider
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
import subprocess
from datetime import datetime
from pymongo import MongoClient

# url = 'https://www.yelp.com/biz/fang-san-francisco-2'

parser = argparse.ArgumentParser(description='Run scrapes')
parser.add_argument('-u')
parser.add_argument('-n')
args = parser.parse_args()

def scrapeReviews(url, restaurant_name):
  # Read in number of reviews
  numReviews = 0
  with open('get_positive/get_positive/reviewCounts.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
      numReviews = int(row[0])

  # Scrape/crawl restaurant on Yelp
  client = MongoClient()
  db = client['reviews_db']
  coll = db['reviews']

  # coll.delete_many({})

  num = 0
  process = CrawlerProcess(get_project_settings())
  process.crawl(yelp_spider, start_url=url,
                             coll=coll,
                             page_num=num,
                             restaurant_name=restaurant_name)
  while num < numReviews:
    process.crawl(yelp_spider, start_url=(url + '?start=' + str(num)),
                               coll=coll,
                               page_num=num,
                               restaurant_name=restaurant_name)
    num += 100

  process.start()

scrapeReviews(args.u, args.n)

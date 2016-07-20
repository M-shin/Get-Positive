import argparse
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

parser = argparse.ArgumentParser('Get counts/name')
parser.add_argument('-u')
args = parser.parse_args()

def getReviewCount(url):
  # Get the number of reviews
  process = CrawlerProcess(get_project_settings())
  process.crawl(review_count_spider, start_url=url)

getReviewCount(args.u)
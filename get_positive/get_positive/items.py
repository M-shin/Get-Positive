# -*- coding: utf-8 -*-

import scrapy

class ReviewCountItem(scrapy.Item):
	count = scrapy.Field()
	pass

class YelpItem(scrapy.Item):
  body = scrapy.Field()
  name = scrapy.Field()
  rating = scrapy.Field()
  url = scrapy.Field()
  pass
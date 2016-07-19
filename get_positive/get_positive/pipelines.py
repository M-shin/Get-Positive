# -*- coding: utf-8 -*-
import json

class YelpPipeline(object):

  def __init__(self):
    self.urls_seen = set()

  # def open_spider(self, spider):
    # print 'spider opened'
    # fileName = 'output.json'
    # self.file = open(fileName, 'wb')

  def process_item(self, item, spider):
    # line = json.dumps(dict(item)) + "\n"
    # self.file.write(line)
    return item
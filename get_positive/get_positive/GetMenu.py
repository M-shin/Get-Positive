import csv
import requests
import json

from pymongo import MongoClient

def getMenuItems():
  name = ''
  zip_code = ''
  with open('get_positive/get_positive/reviewCounts.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
      name = row[1]
      zip_code = row[2]

  data = {
    'api_key': '302cf95a2590d1e89d84bf7d23314e73820f450a',
    'fields': ['menus'],
    'venue_queries': [{
      'name': name,
      'location': {
        'postal_code': zip_code
      }
    }]
  }
  headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
  url = 'https://api.locu.com/v2/venue/search'
  r = requests.post(url, data=json.dumps(data), headers=headers)
  response = r.json()

  # Restaurant/zip code combo not found
  if len(response['venues']) == 0:
  	return 1

  # Get menu items
  menu_items = set([])
  for menu in response['venues']:
    for served_menu in menu['menus']:
      for section in served_menu['sections']:
        for subsection in section['subsections']:
          for content in subsection['contents']:
            if 'name' in content.keys():
              try:
                menu_items.add(str(content['name']))
              except UnicodeEncodeError:
                pass

  menu_items = list(menu_items)

  # Insert into DB
  client = MongoClient()
  db = client['reviews_db']
  coll = db['reviews']
  coll.update_one(
    {'name': name},
    {'$set': {'menuItems': menu_items}}
  )

  return 0

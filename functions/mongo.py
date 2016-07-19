from pymongo import MongoClient

# returns a list of review objects which contain a certain keyword
def search_by_keyword(keyword):
  client = MongoClient()
  coll = client.mockDB.reviews
  cursor = coll.find()
  results = []

  for item in cursor:
    if keyword in item['body']:
      results.append(item)

  return results

# returns a list of review objects which have a certain rating
def search_by_rating(rating):
  client = MongoClient()
  coll = client.mockDB.reviews
  cursor = coll.find()
  results = []

  for item in cursor:
    if float(rating) == float(item['rating']):
      results.append(item)

  return results

# returns a list of review objects which is for a certain restaurant
def search_by_restaurant(restaurant):
  client = MongoClient()
  coll = client.mockDB.reviews
  cursor = coll.find()
  results = []

  for item in cursor:
    if restaurant.lower() == item['name'].lower():
      results.append(item)

  return results

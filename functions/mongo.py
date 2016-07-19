from pymongo import MongoClient

# returns all review objects in database
def get_all_reviews():
  client = MongoClient()
  coll = client.mockDB.reviews
  cursor = coll.find()
  return list(cursor)

# returns a list of review objects which contain a certain keyword
def search_by_keyword(keyword):
  cursor = get_all_reviews()
  results = []

  for item in cursor:
    if keyword in item['body']:
      results.append(item)

  return results

# returns a list of review objects which have a certain rating
def search_by_rating(rating):
  cursor = get_all_reviews()
  results = []

  for item in cursor:
    if float(rating) == float(item['rating']):
      results.append(item)

  return results

# returns a list of review objects which is for a certain restaurant
def search_by_restaurant(restaurant):
  # normalizes whitespace between words to 1 space
  restaurant = ' '.join(restaurant.split())
  cursor = get_all_reviews()
  results = []

  for item in cursor:
    item_name = ' '.join(item['name'].split())
    if restaurant.lower() == item_name.lower():
      results.append(item)

  return results
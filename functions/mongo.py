from pymongo import MongoClient

# returns all restaurant objects in database
# restaurant objects contain name, url, list of reviews, and menu items
def get_all_restaurants():
  client = MongoClient()
  coll = client.mockDB.reviews
  cursor = coll.find()
  return list(cursor)

# returns restaurant object for specified restaurant name
# restaurant objects contain name, url, list of reviews, and menu items
def find_restaurant_info(restaurant_query):
  restaurant_query = ' '.join(restaurant_query.split())
  restaurants = get_all_restaurants()
  results = []
  
  for restaurant in restaurants:
    restaurant_name = ' '.join(restaurant['name'].split())
    if restaurant_query.lower() == restaurant_name.lower():
      results.append(restaurant)

  return results

# returns all review objects in database
# review objects have body and rating
def get_all_reviews():
  reviews = []
  restaurants = get_all_restaurants()
  for restaurant in restaurants:
    for review in restaurant['reviews']:
      reviews.append(review)
  return reviews

# returns a list of review objects which contain a certain keyword
# review objects have body and rating
def search_by_keyword(keyword):
  cursor = get_all_reviews()
  results = []

  for item in cursor:
    if keyword.lower() in item['body'].lower():
      results.append(item)

  return results

# returns a list of review objects which have a certain rating
# review objects have body and rating
def search_by_rating(rating):
  cursor = get_all_reviews()
  results = []

  for item in cursor:
    if float(rating) == float(item['rating']):
      results.append(item)

  return results

# returns a list of restaurant objects which is for a certain restaurant
# review objects have body and rating
def search_by_restaurant(restaurant_query):
  # normalizes whitespace between words to 1 space
  restaurant_query = ' '.join(restaurant_query.split())
  restaurants = get_all_restaurants()
  results = []

  for restaurant in restaurants:
    restaurant_name = ' '.join(restaurant['name'].split())
    if restaurant_query.lower() == restaurant_name.lower():
      for review in restaurant['reviews']:
        results.append(review)

  return results

print get_all_reviews()
from pymongo import MongoClient

client = MongoClient()
coll = client.mockDB.reviews
data = [
  {'rating': '5.0', 'body': 'What an amazing foodie experience at Fang!'},
  {'rating': '3.0', 'body': 'The serious was relatively slow and the main guy was very pushy about his suggestions.'}
]
for datum in data:
  coll.insert(datum)

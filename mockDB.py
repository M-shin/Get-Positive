from pymongo import MongoClient

client = MongoClient()
client.mockDB.reviews.drop()
coll = client.mockDB.reviews
data = [
  {'rating': '5.0', 'name': 'Fang', 'body': 'What an amazing foodie experience at Fang!'},
  {'rating': '3.0', 'name': 'Fang', 'body': 'The serious was relatively slow and the main guy was very pushy about his suggestions.'},
  {'rating': '5.0', 'name': 'Los Hermanos Taqueria', 'body': 'DELICIOUS! It is a little sketchy, just because it\'s literally INSIDE a liquor store, but the lady who took our order was very sweet and giving.'}
]

for datum in data:
  coll.insert(datum)

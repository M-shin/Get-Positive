from pymongo import MongoClient

client = MongoClient()
client.mockDB.reviews.drop()
coll = client.mockDB.reviews
data = [
  {
    'name': 'Fang', 
    'url': 'http://www.yelp.com/biz/fang-san-francisco-2',
    'reviews': [
      {
        'body': 'What an amazing foodie experience at Fang!',
        'rating': 5.0
      },
      {
        'body': 'The serious was relatively slow and the main guy was very pushy about his suggestions.',
        'rating': 3.0
      }
    ],
    'menu_items' : [
      'Fried Potstickers', 'Fried Onioncake', 'Steamed Pork Dumplings'
    ]
  },
  {
    'name': 'Los Hermanos Taqueria',
    'url':'http://www.yelp.com/biz/los-hermanos-taqueria-san-francisco',
    'reviews': [
      {
        'body': 'DELICIOUS! It is a little sketchy, just because it\'s literally INSIDE a liquor store, but the lady who took our order was very sweet and giving.',
        'rating': 5.0
      }
    ],
    'menu_items': [
      'Super Burrito', 'Chicken Caeser Salad', 'Mexican Salads'
    ]
  }
]

for datum in data:
  coll.insert(datum)

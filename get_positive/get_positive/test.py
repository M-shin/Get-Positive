from pymongo import MongoClient

client = MongoClient()
db = client['reviews_db']
coll = db['reviews']

curs = coll.find({})
for item in curs:
	print item
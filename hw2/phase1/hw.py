import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pprint
#import sys

client = MongoClient()
# load the json and transfer into bson
json_data = open('airports.json')
response = json_util.loads(json_data.read())
#data = json_util.loads(response.read())
#data = json_util.loads(response)
# establish a blank database and a blank collection
db = client.airports_database
collection = db.airports_collection
# insert all docs in json into collection
#result = airports_collection.insert_many(data)
result = collection.insert_many(response)
# find the first document in the collection
pprint.pprint(collection.find_one())
#update the value of a field in the first doc in the collection
collection.update_one(
	{ 'carriers': '1' },
	{
	  "$set": {
	      'code': 'BBB'
	}
	}
)
pprint.pprint(collection.find_one())
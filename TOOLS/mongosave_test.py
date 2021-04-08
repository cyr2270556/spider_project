import pymongo

house_client = pymongo.MongoClient("mongodb://localhost:27017/")["runoobdb"]["sites"]

# mongo储存

import pymongo
import random


# pymongo.MongoClient('172.16.132.203:27017')['IP']['STATIC_IP']
class Mongoclient:
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)['cuiworkdb']['Logo20201224']

    def save_data(self, datadict):
        # 传入一个字典存储在mongo
        self.client.insert_one(datadict)
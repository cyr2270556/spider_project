import time

import pymongo
import random


class ProxyPool:
    def __init__(self):
        self.client = pymongo.MongoClient('172.16.132.203:27017')['IP']['STATIC_IP']
        # self.client = pymongo.MongoClient('root')['IP']['STATIC_IP']
        self.random()
        self.count = 0

    def random(self):
        item_list = list(self.client.find({"flag": "1"}))
        if len(item_list) != 0:
            # proxy = item_list[0]
            proxy = random.choice(item_list)
            self.proxy = proxy
        else:
            time.sleep(5)

    def pop(self):
        self.count += 1
        if self.count >= 1:
            self.random()
            # print('ip切换')
            self.count = 0
        return self.proxy

import random

import pymongo
IP_URI = "mongodb://root:root962540@10.0.0.55:27017"
IP_DB = "ip_db"
IP_COL = "vps_static_ip_results"

class ProxyPool:
    def __init__(self):
        self.client = pymongo.MongoClient(IP_URI)[IP_DB][IP_COL]
        self.random()
        self.count = 0

    def random(self):
        item_list = list(self.client.find())
        proxy = 'http://' + random.choice(item_list)['ip']
        self.proxy = proxy

    def pop(self):
        self.count += 1
        if self.count >= 1:
            self.random()
            print('ip切换')
            self.count = 0
        return self.proxy
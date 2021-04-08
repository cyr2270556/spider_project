# redis api

import redis
import json


class Redisclient():
    def __init__(self, db):
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=db)

    def save_category_url(self, category_name, category_url):
        # 储存一个以种类名为名,url为种类url的字符串
        self.r.set(category_name, category_url)
        return print("种类数据已存储")

    def get_category_url(self, category_name):
        # 返回一个以name为名的字典

        return self.r.get(category_name)

    def del_r0_item(self, category_name):
        # 删除一个r0数据
        self.r.delete(category_name)

    def save_page_url(self, category_name, page_url):
        # 储存一个以种类为名，所有页数为值的列表
        self.r.lpush(category_name, page_url)

        return print("页数url已储存")

    def get_page_url(self, category_name):
        # 返回一个页的url
        return self.r.rpop(category_name)

    def save_item_url(self, category_name, url):
        self.r.lpush(category_name, url)

        return print(url)

    def get_item_url(self, category_name):
        # 返回一个logo的url
        return self.r.rpop(category_name)

    def save_dict_url(self, name, dict):
        self.r.hmset(name, dict)

    def get_dict_url(self, name, key):
        return self.r.hmget(name, key)

    def save_one_dict(self, name, key, value):
        self.r.hset(name, key, value)

    def get_one_dict(self, name, key):
        return self.r.hget(name, key)

    def get_keys(self, name):
        return self.r.hgetall(name)


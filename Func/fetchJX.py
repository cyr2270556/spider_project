import random
import time

import requests
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *
from Func.get_ip import *
from requests.adapters import HTTPAdapter

# from fake_useragent import UserAgent

# from dgg_dianping_web.dgg_dianping_web.verify import verify_ip

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)


class FETCH(object):
    def __init__(self):
        self.session = requests.session()
        self.s = HTMLSession()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.session.keep_alive = False
        self.client = ProxyPool()
        self.col = ProxyPool().client

    def fetch(self, url, headers=None, data=None, method='get'):
        c = self.client.pop()
        proxy = {'http': 'http://' + c['ip_parmas'], 'https': 'https://' + c['ip_parmas']}
        print(proxy)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }
        if method == 'get':
            try:
                r = self.s.get(url, headers=headers, timeout=10, proxies=proxy)
                # r = requests.get(url, headers=headers, timeout=5, proxies=proxies)
                print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200:
                    r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 404:
                    return None
                else:
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    # return self.fetch(url=url, data=data, headers=headers, method='get')
                    return self.fetch(url=url, headers=headers, method='get')
            except:
                self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                # return self.fetch(url=url, data=data, headers=headers, method='get')
                return self.fetch(url=url, headers=headers, method='get')
        elif method == 'post':
            try:
                r = self.session.post(url, headers=headers, timeout=60, data=data)
                # print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200:
                    # r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 404:
                    pass
                else:
                    # self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    return self.fetch(url=url, data=data, headers=headers, method='post')
            except Exception as e:
                print(e)
                # self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                return self.fetch(url=url, data=data, headers=headers, method='post')

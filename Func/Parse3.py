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


class FETCH3(object):
    def __init__(self):
        self.session = requests.session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.client = ProxyPool()
        self.col = ProxyPool().client

    def fetch3(self, url, headers=None, data=None, method='post'):
        c = self.client.pop()
        proxy = {'http': 'http://' + c['ip_parmas'], 'https': 'https://' + c['ip_parmas']}
        # print(proxy)

        if method == 'post':
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            }
            try:
                r = requests.post(url, headers=headers, timeout=10, data=data, proxies=proxy)
                print('当前请求的Url为：', url, r.status_code, proxy)
                if r.status_code == 200:
                    # r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 404:
                    pass
                else:
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    return self.fetch3(url=url, data=data, headers=headers, method='post')
            except Exception as e:
                print(e)
                self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                return self.fetch3(url=url, data=data, headers=headers, method='post')

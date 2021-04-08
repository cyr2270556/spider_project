import requests
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *
from requests.adapters import HTTPAdapter
from Func.get_ip import *

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

    def fetch(self, url, headers=None, params=None, method='get'):
        c = self.client.pop()
        proxy = {'http': 'http://' + c['ip_parmas'], 'https': 'https://' + c['ip_parmas']}
        print(proxy)
        if method == 'get':
            try:
                r = requests.get(url, timeout=10, headers=headers, proxies=proxy, params=params)
                # r = requests.get(url, headers=headers, timeout=5, proxies=proxies)
                print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200:
                    # r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 404:
                    pass
                else:
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    return self.fetch(url, headers=headers, params=params)
            except Exception as e:
                print(e, '方')
                self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                return self.fetch(url, headers=headers, params=params)

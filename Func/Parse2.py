import re
import time
import random
from urllib import parse

import requests
from requests.adapters import HTTPAdapter
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *
from Func.get_ip import *
from fake_useragent import UserAgent

# from dgg_dianping_web.dgg_dianping_web.verify import verify_ip

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)


class FETCH(object):
    def __init__(self):
        self.s = HTMLSession()
        # requests.adapters.DEFAULT_RETRIES = 5
        self.session = requests.session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.session.keep_alive = False
        self.client = ProxyPool()
        self.col = ProxyPool().client

    def fetch(self, url, headers=None, data=None, method='get'):
        c = self.client.pop()
        proxy = {'http': 'http://' + c['ip_parmas'], 'https': 'https://' + c['ip_parmas']}
        if method == 'get':
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                'Host': 'aiqicha.baidu.com',
                'Connection': 'keep-alive',
            }
            try:
                # r = self.s.get(url, headers=headers, timeout=10)
                r = self.session.get(url, headers=headers, timeout=5, proxies=proxy)
                print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200:
                    r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 404:
                    pass
                elif '白屏时间' in r.text.replace('\/', '/').encode('UTF-8').decode('unicode_escape'):
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    return self.fetch(url=url, data=data, headers=headers, method='get')
                else:
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    return self.fetch(url=url, data=data, headers=headers, method='get')
            except Exception as e:
                print(e)
                self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                return self.fetch(url=url, data=data, headers=headers, method='get')

        elif method == 'GET':
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                'Host': 'aiqicha.baidu.com',
                'Connection': 'keep-alive',
            }
            try:
                r = self.session.get(url, headers=headers, timeout=20, proxies=proxy)
                print(proxy)
                # r = self.s.get(url, headers=headers, timeout=5)
                print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200 and r.json()['status'] == 0:
                    r.encoding = r.apparent_encoding
                    print(r.json()['status'])
                    return r
                elif r.status_code == 200 and r.json()['status'] != 0:
                    print(r.json()['status'])
                    return self.fetch(url, method='GET')
                elif r.status_code == 404:
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    return self.fetch(url)
                elif '白屏时间' in r.text.replace('\/', '/').encode('UTF-8').decode('unicode_escape'):
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    return self.fetch(url, method='GET')
                else:
                    self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    raise Exception
            except Exception as e:
                print(e, '方修坤')
                self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                # print('解析错误，重新发起请求：')
                return self.fetch(url, method='GET')

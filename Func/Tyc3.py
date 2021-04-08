import random

import requests
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *
from Func.get_ip import *

# from fake_useragent import UserAgent

# from dgg_dianping_web.dgg_dianping_web.verify import verify_ip

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)


class FETCH1(object):
    def __init__(self):
        self.session = HTMLSession()
        self.client = ProxyPool()
        self.col = ProxyPool().client
        # self.ua = UserAgent()

    def get_authorization_list(self):
        authorization_list = [
            '0###oo34J0QvMFOOvaXx_nVrQ_n52DdE###1573893411729###d3bd40bddd6391e5ace47fce7a67c79f',
            # '0###oo34J0WVDdeu_k1O-sWPxFpg9WJ4###1555940540033###028a568b0150721d810d5f4417e03650',
            '0###oo34J0elVC8VjCWPRMm9eZVGmL1o###1573452780296###399f51c4fa19a9a12234b7b40b80586f',

        ]
        authorization = random.choice(authorization_list)
        return authorization

    def fetch1(self, url, headers=None, data=None, method='get'):
        b = self.get_authorization_list()
        # print(b)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            # 'authorization': '0###oo34J0RzWPZcJVyheiNc4U9Zeuwc###1581492624852###41085424df0d30e7a30f8afc3bddb464',
            'authorization': b,
            # 'Referer': 'https://servicewechat.com/wx9f2867fc22873452/31/page-frame.html',
            'Host': 'api9.tianyancha.com',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'version': 'TYC-XCX-WX',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        proxies = self.client.pop()['ip_parmas']
        _id = self.client.pop()['_id']
        proxy = {'http': 'http://' + proxies, 'https': 'https://' + proxies}
        print(proxy)
        if method == 'get':
            try:
                # 请求加代理
                # r = self.session.get(url, headers=headers, timeout=5, proxies=proxies)
                # 本地ip请求
                r = self.session.get(url, headers=headers, proxies=proxy)
                print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200:
                    r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 416 or r.status_code == 400:
                    self.col.find_one_and_update({"_id": _id}, {"$set": {"flag": "0"}})
                    return self.fetch1(url)
                else:

                    raise requests.HTTPError
            except Exception as e:
                print(e)
                self.col.find_one_and_update({"_id": _id}, {"$set": {"flag": "0"}})
                # print('解析错误，重新发起请求：')
                return self.fetch1(url)

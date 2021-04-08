import random

import requests
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *
from Func.get_ip import *
from requests.adapters import HTTPAdapter
# from fake_useragent import UserAgent

# from dgg_dianping_web.dgg_dianping_web.verify import verify_ip

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)


class FETCH1(object):
    def __init__(self):
        self.session = requests.session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.session.keep_alive = False
        # self.session = HTMLSession()
        self.client = ProxyPool()
        self.col = ProxyPool().client

    def get_authorization_list(self):
        authorization_list = [
            '0###oo34J0XG6_YVh4XDYNaCaNLnYVYU###1587614353100###a80e260963a23e74073422ffec829bac',
            '0###oo34J0aaAKlX394lVVQgOCTAgrLU###1587608133708###abdacba0a206c9318d82c82045a0dde4',
            # '0###oo34J0WVDdeu_k1O-sWPxFpg9WJ4###1555940540033###028a568b0150721d810d5f4417e03650',
            '0###oo34J0elVC8VjCWPRMm9eZVGmL1o###1573452780296###399f51c4fa19a9a12234b7b40b80586f',
            '0###oo34J0e8mqLUE9n9uO-B-G69upFA###1573452726341###4abc9ab55598b1c410d1e4df40ada271',
            '0###oo34J0V58gXuFBdhZidO9AN1ZYCc###1586917020928###0ce411d6bd4bc3c8b75e868c5323ac4e',
            '0###oo34J0QvMFOOvaXx_nVrQ_n52DdE###1573893411729###d3bd40bddd6391e5ace47fce7a67c79f',
            '0###oo34J0e7F5rz2IGvVRA00L7HVXEo###1586831123569###de131a38ec0509f1f6344410ea0db56b',
            '0###oo34J0RzWPZcJVyheiNc4U9Zeuwc###1587432420346###41085424df0d30e7a30f8afc3bddb464',
            ''

        ]
        authorization = random.choice(authorization_list)
        return authorization

    def fetch1(self, url, companyName):
        b = self.get_authorization_list()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorization': b,
            # 'Referer': 'https://servicewechat.com/wx9f2867fc22873452/31/page-frame.html',
            'Host': 'api9.tianyancha.com',
            # 'Connection': 'keep-alive',
            'content-type': 'application/json',
            'version': 'TYC-XCX-WX',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        data = {
            "keyWords": companyName,
            "pn": 1,
            "ps": 30,
            "casereason": -100
        }
        c = self.client.pop()
        proxy = {'http': 'http://' + c['ip_parmas'], 'https': 'https://' + c['ip_parmas']}
        print(proxy, b)

        try:
            r = self.session.post(url, headers=headers, json=data, proxies=proxy, timeout=5)
            # print(r.status_code)
            print('当前请求的Url为：', url, r.status_code)
            if r.status_code == 200:
                # r.encoding = r.apparent_encoding
                return r
            elif r.status_code == 416:
                self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                return self.fetch1(url, companyName)
            elif r.status_code == 401:
                # self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                return self.fetch1(url, companyName)
            elif r.status_code == 404 or r.status_code == 400:
                pass
            else:
                self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                return self.fetch1(url, companyName)
        except Exception as e:
            print(e)
            self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
            # print('解析错误，重新发起请求：')
            return self.fetch1(url, companyName)

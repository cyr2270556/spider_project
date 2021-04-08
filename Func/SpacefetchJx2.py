import random
import time

import requests
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *

# from fake_useragent import UserAgent

# from dgg_dianping_web.dgg_dianping_web.verify import verify_ip

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)


class FETCH1(object):
    def __init__(self):
        self.session = HTMLSession()
        # self.ua = UserAgent()

    # def get_ip(self):
    #     # ip_list = [
    #     #     '10.0.0.51:9999',
    #     #     '10.0.0.52:9999',
    #     #     '10.0.0.53:9999',
    #     #     '10.0.0.54:9999',
    #     #     '10.0.0.55:9999',
    #     # ]
    #     # ip = random.choice(ip_list)
    #     # proxy = {'http': 'http://' + ip, 'https': 'https://' + ip}
    #     # return proxy
    #     try:
    #         ip = redis.ldelete('ips')
    #         proxy = {'http': 'http://' + ip, 'https': 'https://' + ip}
    #         return proxy
    #     except:
    #         time.sleep(6)
    #         self.get_ip()
    def ABY_IP_(self):
        """#
        阿布云代理接入
        :return:
        """
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "HQ74H343NC8P83MD"
        proxyPass = "72425EBF9493543B"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        # print(proxies)
        return proxies

    def postfetch(self, url, headers=None, data=None, method='get'):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Referer': 'https://shop.10086.cn/i/?f=rechargegprs&mobileNo=18437975168&amount=1024',
        }

        proxies = self.ABY_IP_()

        try:
            r = self.session.post(url, headers=headers, json=data, timeout=5, proxies=proxies)
            # r = requests.post(url, headers=headers, json=data, timeout=5, proxies=proxies)
            print('当前请求的Url为：', url)
            if r.status_code == 200:
                r.encoding = r.apparent_encoding
                return r
            else:
                raise Exception
        except:
            # print('解析错误，重新发起请求：')
            return self.postfetch(url)

import random
import time

import requests
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *
# from fake_useragent import UserAgent

# from dgg_dianping_web.dgg_dianping_web.verify import verify_ip

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)


class FETCH(object):
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

    def fetch(self, url, headers=None, data=None, method='get'):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            # 'Cookie': 'UM_distinctid=16c26ae0a80b90-08efad43f7c115-c343162-1fa400-16c26ae0a81acb; zg_did=%7B%22did%22%3A%20%2216c26ae0b172f3-07ada9149a069b-c343162-1fa400-16c26ae0b18b16%22%7D; _uab_collina=156401703613463264358483; acw_tc=3a31f81e15772647621805678e94afffcd0d54e7ab80a0156890ab2611;'
            'Referer': 'https://shop.10086.cn/i/?f=rechargegprs&mobileNo=18437975168&amount=1024',
            # 'Cookie': 'inx=myorders; inx2=returnorderqry; collect_id=vfd25gy3jdqcirjpqdg3q5ua1w67nu5a; _gscu_1502255179=68279588ocps2n18; CmLocation=280|280; CmProvid=bj; WT_FPC=id=26fb0f6fcf1dd1f0b3b1567126683115:lv=1579161975894:ss=1579161975894; jsessionid-echd-cpt-cmcc-jt=49FDE9C17750148E26EC13EBC1D8B5A7; arp_scroll_position=600'
        }

        proxies = self.ABY_IP_()
        if method == 'get':
            try:
                r = self.session.get(url, headers=headers, timeout=5, proxies=proxies)
                # r = requests.get(url, headers=headers, timeout=5, proxies=proxies)
                # print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200:
                    r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 403:
                    pass
                else:
                    raise requests.HTTPError
            except:
                # print('解析错误，重新发起请求：')
                return self.fetch(url)
        elif method == 'post':
            try:
                # r = self.session.post(url, headers=headers,data=data, timeout=5,proxies=proxies)
                r = requests.post(url, headers=headers, json=data, timeout=5,proxies=proxies)
                print('当前请求的Url为：', url)
                if r.status_code == 200:
                    r.encoding = r.apparent_encoding
                    return r
                else:
                    raise Exception
            except:
                # print('解析错误，重新发起请求：')
                return self.fetch(url)

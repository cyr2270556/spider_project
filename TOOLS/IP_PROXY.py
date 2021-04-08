import requests
import time
import json

# ip接口
# url = 'http://xxxx.asiyun.cn/api/getIp?type=&num=&pid=&cid=&orderId=&time=&sign=&dataType=&singleIp='
# post_time = time.time() / 1000
# post_data = {
#     "orderId": "",
#     "time": post_time,
#     "sign": "",
#     "num": "",
#     "type": "HTTP/HTTPS",
#     "pid": "",
#     "cid": "",
#     # 绑定时长，单位秒，可选值 60、180、300、600、900、 1800，不填默认60
#     "unbindTime": "",
#     # 0:不去重，1:24小时去重，不 填默认0
#     "noDuplicate": "",
# }
"""
{"realIp":"123.174.70.244","pid":12,"cid":111,"area":"山西-运城","ip":"x.x.x.x","port":x}

realIp为此次代理出口真实ip

area 为ip归属地域   

ip和port为此次代理请求发送的ip和端口。实际出口为realIp

"""
#
# res_json=requests.get(url,post_data)
# res=json.loads(res_json.json())
# print(res["ip"])

a = {"realIp": "123.174.70.244", "pid": 12, "cid": 111, "area": "山西-运城", "ip": "x.x.x.x", "port": "x"}
res_json = json.dumps(a)
res = json.loads(res_json)
ip = res["ip"] + ":" + res["port"]
print(ip)

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

# redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)


class API_FETCH(object):
    def __init__(self,post_time):
        self.session = requests.session()
        self.s = HTMLSession()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.session.keep_alive = False
        self.ip_url='http://xxxx.asiyun.cn/api/getIp?type=&num=&pid=&cid=&orderId=&time=&sign=&dataType=&singleIp='
        self.post_data = {
            "orderId": "",
            "time": post_time,
            "sign": "",
            "num": "",
            "type": "HTTP/HTTPS",
            "pid": "",
            "cid": "",
            # 绑定时长，单位秒，可选值 60、180、300、600、900、 1800，不填默认60
            "unbindTime": "",
            # 0:不去重，1:24小时去重，不 填默认0
            "noDuplicate": "",
        }

    def get_ip(self):
        res_json = requests.get(self.ip_url, self.post_data)
        res = json.loads(res_json.json())
        ip = res["ip"] + ":" + res["port"]
        return ip

    def fetch(self, url, headers=None, data=None, method='get'):
        ip=self.get_ip()
        proxy = {'http': 'http://' + ip, 'https': 'https://' + ip}
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
                   # self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
                    # return self.fetch(url=url, data=data, headers=headers, method='get')
                    return self.fetch(url=url, headers=headers, method='get')
            except:
                #self.col.find_one_and_update({"_id": c['_id']}, {"$set": {"flag": "0"}})
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
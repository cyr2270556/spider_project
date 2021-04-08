import time
import requests
from requests_html import HTMLSession
from Func.Redis import REDIS
from Func.conf import *
from fake_useragent import UserAgent

# from dgg_dianping_web.dgg_dianping_web.verify import verify_ip

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=ipDB)

class FETCH(object):
    def __init__(self):
        self.session = HTMLSession()
        self.ua = UserAgent()

    def get_ip(self):
        try:
            ip = redis.ldelete('ips')
            proxy = {'http': 'http://' + ip, 'https': 'https://' + ip}
            return proxy
        except:
            time.sleep(6)
            self.get_ip()

    def fetch(self, url, headers=None, data=None, method='get'):
        if 'baidu.com' in url:
            headers = {
                'User-Agent': self.ua.random,
            }
        elif 'sogou' in url:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
                # 'User-Agent': self.ua.random,
                'Referer': url
                # 'cookie': 'Hm_lvt_5044dcecc06da18b0a2734969e386b57=1557043245,1557196673; Apache=75cba780.588431aa40089; 77232___866562_KS_77232___866562=43c0aa2fc10344de82c817eb4265564c; 76481___940766_KS_76481___940766=22c261e5f0c046ea93a24402bee9ebe1; 77744___779046_KS_77744___779046=51852fb26be8456db192ba3aed7fb703; 77232___866562_curPageNum=8; PHPSESSID=aqiqm0r6fg0ov448mtif6o15a7; Hm_lvt_0c0543187cc8155dc935d6dbba47fc3c=1557709958,1557719357,1557731576,1557796108; WK786d_pre_url=http%3A%2F%2F; WK786d_historys=a%3A4%3A%7Bi%3A0%3Ba%3A5%3A%7Bs%3A8%3A%22goods_id%22%3Bs%3A7%3A%221819455%22%3Bs%3A4%3A%22type%22%3Bi%3A4%3Bs%3A6%3A%22number%22%3Bi%3A1%3Bs%3A4%3A%22date%22%3Bs%3A19%3A%222019-05-14+09%3A08%3A21%22%3Bs%3A11%3A%22staff_style%22%3Bi%3A1%3B%7Di%3A1%3Ba%3A5%3A%7Bs%3A8%3A%22goods_id%22%3Bs%3A7%3A%221613938%22%3Bs%3A4%3A%22type%22%3Bi%3A4%3Bs%3A6%3A%22number%22%3Bi%3A1%3Bs%3A4%3A%22date%22%3Bs%3A19%3A%222019-05-14+09%3A39%3A04%22%3Bs%3A11%3A%22staff_style%22%3Bi%3A1%3B%7Di%3A2%3Ba%3A5%3A%7Bs%3A8%3A%22goods_id%22%3Bs%3A6%3A%22229259%22%3Bs%3A4%3A%22type%22%3Bi%3A4%3Bs%3A6%3A%22number%22%3Bi%3A2%3Bs%3A4%3A%22date%22%3Bs%3A19%3A%222019-05-14+09%3A42%3A55%22%3Bs%3A11%3A%22staff_style%22%3Bi%3A1%3B%7Di%3A3%3Ba%3A5%3A%7Bs%3A8%3A%22goods_id%22%3Bs%3A7%3A%222020018%22%3Bs%3A4%3A%22type%22%3Bi%3A4%3Bs%3A6%3A%22number%22%3Bi%3A1%3Bs%3A4%3A%22date%22%3Bs%3A19%3A%222019-05-14+09%3A47%3A12%22%3Bs%3A11%3A%22staff_style%22%3Bi%3A1%3B%7D%7D;'
            }
        elif 'm.sm.cn' in url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                'referer': 'https://m.sm.cn/'
            }
        proxies = self.get_ip()
        if method == 'get':
            try:
                r = self.session.get(url, headers=headers, proxies=proxies, data=data, timeout=5)
                print('当前请求的Url为：', url, r.status_code)
                if r.status_code == 200:
                    r.encoding = r.apparent_encoding
                    return r
                elif r.status_code == 404:
                    pass
                else:
                    raise requests.HTTPError
            except:
                # print('解析错误，重新发起请求：')
                return self.fetch(url)
        elif method == 'post':
            try:
                r = self.session.post(url, headers=headers, proxies=proxies, data=data, timeout=5)
                print('当前请求的Url为：', url)
                if r.status_code == 200:
                    r.encoding = r.apparent_encoding
                    return r
                else:
                    raise Exception
            except:
                # print('解析错误，重新发起请求：')
                return self.fetch(url)
    def fecth1(self,url):
        headers = {
            'User-Agent': self.ua.random,
            # 'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
            # 'Referer': url,
            # 'Host': 'www.so.com',
            # 'X-Requested-With': 'XMLHttpRequest',
            # 'Cookie': 'QiHooGUID=E9C9210A413486F1DF36CF1EC3EA3B41.1561345088480; __guid=15484592.2372949039577771500.1561345090241.173; webp=1; stc_ls_sohome=RgzW2OYRKZ!pTRX4hnM(Wd; __huid=11%2Bj%2FkALLZqCpNYfc3Frtzad%2FFUhjgXAkuUvaPc63p7Pg%3D; dpr=1; screenw=1; env_webp=1; Qs_lvt_100433=1561373153; gtHuid=1; Qs_pv_100433=4132035465581699000%2C801767428391377300%2C501088628690619650%2C1643312176685093000; arp_scroll_position=0;'

        }
        try:
            r = requests.get(url, headers=headers, timeout=5)
            print('当前请求的Url为：', url, r.status_code)
            if r.status_code == 200:
                r.encoding = r.apparent_encoding
                return r
            elif r.status_code == 404:
                pass
            else:
                raise requests.HTTPError
        except:
            # print('解析错误，重新发起请求：')
            return self.fetch(url)


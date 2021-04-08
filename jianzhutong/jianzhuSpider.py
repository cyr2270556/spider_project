from time import sleep
import requests
from lxml import etree
from Func.fetchJX import FETCH
from TOOLS.md5encode import md5encryption,is_phone
from Func.client import MongoDB
from TOOLS.redissave import Redisclient
import re


class JanzhuSpider():
    def __init__(self, start_url,cookie,referer,companyCity,companyProvince,db):
        self.start_url = start_url
        self.companyCity = companyCity
        self.companyProvince = companyProvince
        self.headers = {

            # ":authority":"www.cbi360.net",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cookie":cookie,
            # "Cookie": "",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests":"1",
            "Referer" : referer,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",

        }
        self.r0 = Redisclient(0)
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', db)
        # self.f = FETCH()
        self.par = re.compile(r'\d+-\d+')
        self.par2 = re.compile(r'\d+')

    def parse_next_page(self):
        self.r0.save_page_url(category_name="北京", page_url=self.start_url)
        # html = self.f.fetch(url=self.start_url, headers=self.headers, method='get')
        html = requests.get(url=self.start_url,headers=self.headers)
        sleep(2)
        while True:
            res = etree.HTML(html.text)
            try:
                next_page = res.xpath('//ul[@class="pagination"]//li//a[contains(text(),"下一页")]/@href')
                print(next_page)
                next_page='https://www.cbi360.net'+next_page[0]
            except Exception as e:
                print(e)
                print(html.text)
                break
            self.r0.save_page_url(category_name="北京", page_url=next_page)
            self.parse_item(res)
            # html = self.f.fetch(url=next_page, headers=self.headers, method='get')
            html = requests.get(url=next_page, headers=self.headers)
            sleep(1)

    def re_phone(self, target):
        try:
            phone = re.findall(self.par, target)[0]
        except:
            print(target)
            try:
                phone = re.findall(self.par2, target)[0]
            except:
                phone = ''
        return phone

    def parse_item(self,res):
        # //dl[@class="table—con-bottom clear"]//dd[@class="w-18"][2]
        # while True:
            # try:
            #     # url = self.r0.get_page_url(category_name='北京')
            #     # html = self.f.fetch(url=url, headers=self.headers, method='get')
            #     # html = requests.get(url=url, headers=self.headers)
            # except:
            #     continue
        sleep(1)
            # res = etree.HTML(html.text)
        companyName_list = res.xpath(
            '//ul[@class="table-con-top clear search-word"]//li[@style]//preceding-sibling::* //a[@target="_blank"]/text()')
        phone_list = res.xpath('//dl[@class="table—con-bottom clear"]//dd[@class="w-18"][2]/text()')
        for i in range(len(companyName_list)):
            item = {}
            companyName = companyName_list[i]
            phone = self.re_phone(phone_list[i])
            if is_phone(phone):
                item['companyCity'] = self.companyCity
                item['companyProvince'] = self.companyProvince
                item['code'] = 'BUS_YT_ZZ'
                item['name'] = '资质'
                item['busCode'] = ''
                item['webUrl'] = '无'
                item['orgId'] = ''
                item['deptId'] = ''
                item['centreId'] = ''
                item["companyName"] = companyName
                item["outName"] = ''
                item["resourceRemark"] = ''
                item["companyTel"] = phone
                item["ibossNum"] = None
                item['isDir'] = 0
                item['isShare'] = 0
                item["_id"] = md5encryption(item["companyTel"])
                item["flag"] = 0
                print(item)
                self.m.mongo_add(item)

    def run(self):
        self.parse_next_page()

if __name__ == '__main__':
    spider = JanzhuSpider(

        start_url='https://www.cbi360.net/hhb/companysoso/?provinceid=410000&searchmatch=2&compareid=0&layer=true&anchor=false',
        cookie='cbi360_province=%e5%9b%9b%e5%b7%9d; UM_distinctid=176e5776c66c7-096cd8032d011c-303464-1fa400-176e5776c67961; CNZZDATA30036250=cnzz_eid%3D1704198305-1610164664-%26ntime%3D1610516275; ad_s_u_t_0105=2; ad_s_v_t_0105=4; ad_lb_u_t_0105=2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%220e7e7d39-8d6f-49df-a30b-bdfc17f629b9%22%2C%22first_id%22%3A%22176e56e8709251-0cb6f5d6af0abf-303464-2073600-176e56e870a3dd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22176e56e8709251-0cb6f5d6af0abf-303464-2073600-176e56e870a3dd%22%7D; Hm_lvt_680d256f97e094a807ba2e598bd502f9=1611971734,1612140885,1612228344,1612418347; Hm_lvt_9f1a930c5ecc26fe983d898c26bd5fea=1611971734,1612140885,1612228344,1612418347; cbi360=accesstoken=6F1CC1B156878CC13EDFA70C5E3CBAF58742777FDF413E474C3C1C6B626175CBC2CB0CE747E6E3D677C134F67A9D625153A5786969378E4A&expiretime=1900-01-01&ishistoryvip=0&isvip=2&nickname=cyr&parentuseraccount=13258399376&parentuserid=89CD03A595A478BE0B639A5EDF6E656F3ACD106AF5F1EB82508933DEFBC0DBD137336A54500600B0&province=%e5%9b%9b%e5%b7%9d&sign=024361d9510f84a8&token=9ca33c44051b4138bc4fcc90dedb0230&uid=b4f3c10a67c093c8&uidsign=56b259a1db5136fc&useraccount=13258399376&userid=89CD03A595A478BE0B639A5EDF6E656F3ACD106AF5F1EB82508933DEFBC0DBD137336A54500600B0&username=cyr&viplevel=&wxlogin=True; Hm_lvt_2c83b793310ff6a04ed72f97dfc92eb9=1612140885,1612228344,1612418347,1612418409; Hm_lpvt_9f1a930c5ecc26fe983d898c26bd5fea=1612427085; Hm_lpvt_2c83b793310ff6a04ed72f97dfc92eb9=1612427085; Hm_lpvt_680d256f97e094a807ba2e598bd502f9=1612427085; arp_scroll_position=200',
        referer='https://www.cbi360.net/hhb/companysoso/?provinceid=440000&searchmatch=2&compareid=0&layer=true&anchor=false',
        companyCity='郑州',
        companyProvince='河南省',
        db="jianzhutong_henan"

    )
    spider.run()
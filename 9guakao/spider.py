#9挂靠网

import os
import requests
from TOOLS.md5encode import md5encryption,is_phone
from TOOLS.mongosave import MongoDB
from TOOLS.redissave import Redisclient
from lxml import etree
from PIL import Image
import pytesseract
from Func.fetchJX import FETCH
from Func.client import MongoDB

import base64
import sys
from time import sleep
#http://www.9gk.cc/zp/shanghai/p1700
#http://www.9gk.cc/zp/shanghai/p1713

class Spider9():
    def __init__(self):
        self.start_url = 'http://www.9gk.cc/zp/sichuan/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'
        }

        self.headers_fordata={

            # ":authority":"www.cbi360.net",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cookie": "Hm_lvt_ccf8b732d64d55d0d8a73ec2bcd276ab=1612144130,1612399856,1612752316,1613704044; Hm_lpvt_ccf8b732d64d55d0d8a73ec2bcd276ab=1613704100",
            "Connection": "keep-alive",
            "Host":"www.9gk.cc",
            "pragma": "no-cache",
            "Referer": "http://www.9gk.cc/zp/p1700",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",

        }
        self.r0 = Redisclient(0)
        self.r1 = Redisclient(1)
        self.r2 = Redisclient(2)
        self.f = FETCH()
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', "9guakao_chengdu")

    def get_category_url(self):
        for i in range(14):
            url = self.start_url+"p"+str(1700+i)
            self.r0.save_page_url("上海",url)

    def get_all_page(self):
        while True:
            try:
                url = self.r0.get_page_url("上海")
            except:
                break
            #/page/2
            self.r1.save_page_url("上海",url)
            try:
                html = requests.get(url=url,headers=self.headers)
            except:
                break
            print(html.text)
            res = etree.HTML(html.text)
            try:
                last_page = res.xpath('//ul[@class="pagination"]//li[@class="disable"]//following-sibling::li//a/text()')
                if last_page==[]:
                    last_page = list(res.xpath('//ul[@class="pagination"]//li//a/text()')[-1])
            except Exception as e:
                print(e)
                break
            for i in range(2, int(last_page[0])+1):
                page_url = str(url,"utf-8")+r'/page/{}'.format(i)
                self.r1.save_page_url("上海", page_url)

    def parse_item_url(self):
        #//div[@class="col-xs-12 boxshadow"]//div[@class="col-lg-12 bk-btm-xuxian pad-10"]//div[@class="col-lg-5 pad-left20"]//a/@href
        while True:
            try:
                url=self.r1.get_page_url("上海")
                html = requests.get(url=url, headers=self.headers)
            except Exception as e:
                break

            # print(html.text)
            res = etree.HTML(html.text)
            # item_url_list = res.xpath('//div[@class="col-xs-12  boxshadow "]//div[@class="col-lg-12 bk-btm-xuxian pad-10"]//div[@class="col-lg-5 pad-left20"]//a/@href')
            item_url_list = res.xpath('/html/body/div[5]/div/div/div/span/a/@href')
            for i in range(len(item_url_list)):
                print(item_url_list[i])
                self.r2.save_page_url("上海", item_url_list[i])

    def parse_data(self):
        while True:
            try:
                url = self.r2.get_page_url("上海")
                print(url)
            except:
                break
            headers = self.headers_fordata
            headers["Referer"] = url
            html = requests.get(url=url, headers=headers)
            res = etree.HTML(html.text)
            try:
                outName = res.xpath('/html/body/div[3]/div[1]/div[2]/div[4]/text()')[0]
                phone = res.xpath('/html/body/div[3]/div[1]/div[2]/div[6]/span/text()')[0]
                companyName = res.xpath('/html/body/div[3]/div[1]/div[1]/h2/text()')[0]
            except:
                continue
            if is_phone(phone):
                if "企业管理" not in str(companyName):
                    print(companyName)
                    item={}
                    item['companyCity'] = "成都"
                    item['companyProvince'] = "四川省"
                    item['code'] = 'BUS_YT_ZZ'
                    item['name'] = '资质'
                    item['busCode'] = ''
                    item['webUrl'] = '无'
                    item['orgId'] = ''
                    item['deptId'] = ''
                    item['centreId'] = ''
                    item["companyName"] = companyName
                    item["outName"] = outName
                    item["resourceRemark"] = ''
                    item["companyTel"] = str(phone)
                    item["ibossNum"] = None
                    item['isDir'] = 0
                    item['isShare'] = 0
                    item["_id"] = md5encryption(item["companyTel"])
                    # item["flag"] = 0
                    print(item)
                    self.m.mongo_add(item)
            else:
                continue
    def run(self):
        self.get_category_url()
        self.get_all_page()
        self.parse_item_url()
        self.parse_data()

    def test(self):
        pass

if __name__ == '__main__':
    s = Spider9()
    s.run()


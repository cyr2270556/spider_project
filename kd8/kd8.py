from bs4 import BeautifulSoup
from lxml import etree
from Func.fetchJX import FETCH
from Func.client import MongoDB
from time import sleep
from TOOLS.redissave import Redisclient
import re

import requests


# 需求：姓名+企业基本信息+联系方式

# print(html_doc.text)
# soup = BeautifulSoup(html_doc.content, "lxml",from_encoding='utf-8')
# print(soup.find_all('a'))


class Spider_kd8():
    def __init__(self):
        self.start_url = 'http://www.qd8.com.cn/index.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.s = FETCH()
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', "78guakao")
        self.r0 = Redisclient(0)
        self.r1 = Redisclient(1)
        self.r2 = Redisclient(2)
        self.category_name_list = []
        self.sec_category_name_list = []

    def get_category_url(self):
        # html = self.s.fetch(url=self.start_url, method='get')
        html = requests.get(url=self.start_url, headers=self.headers)
        res = etree.HTML(html.text)
        category = res.xpath('//table//tr//div[@class="citylist"]//span')
        for i in category:
            category_name = i.xpath('./a/font/text()')
            if category_name == []:
                category_name = i.xpath('./a/text()')
            category_url = i.xpath('./a/@href')
            print(category_name)
            print(category_url)

            self.category_name_list.append(category_name[0])
            self.r0.save_category_url(category_name=category_name[0], category_url=category_url[0])

    def get_second_category_url(self):
        for city in self.category_name_list:
            print(city)
            category_url = self.r0.get_category_url(city).decode()
            # html = self.s.fetch(url=category_url, method='get')
            html = requests.get(url=category_url, headers=self.headers)
            res = etree.HTML(html.text)
            sec_category_list = res.xpath('//div[@class="nav"]//a')[1:]
            one_city_dict = {}
            for one in sec_category_list:
                sec_category_name = one.xpath('./text()')[0]
                sec_category_url = one.xpath('./@href')[0]
                print(sec_category_name)
                print(sec_category_url)
                self.sec_category_name_list.append(sec_category_name)
                one_city_dict[sec_category_name] = category_url + sec_category_url[1:]
            self.r1.save_dict_url(city, one_city_dict)


    def get_third_category(self):
        dict_data={}
        for city in self.category_name_list:
            for k in self.sec_category_name_list:
                url = self.r1.get_dict_url(city, k)[0]
                html = requests.get(url=url, headers=self.headers)
                res = etree.HTML(html.text)
                third_category_list = res.xpath('//div[@class="jzlianjie"]//a')
                for one in third_category_list:
                    third_category_name = one.xpath('./text()')
                    third_category_url = one.xpath('./@href')
                    print(third_category_name[0])
                    head = self.r0.get_category_url(city).decode()
                    all = head + third_category_url[0][1:]
                    dict_data[third_category_name[0]]=all
                    # http://aomen.qd8.com.cn/xunchongwu/

                self.r2.save_dict_url(city+k,dict_data)



    def run(self):
        self.get_category_url()
        self.get_second_category_url()
        self.get_third_category()


if __name__ == '__main__':
    spider = Spider_kd8()
    spider.run()

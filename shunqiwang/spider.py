# 顺企网
from TOOLS.mongosave import MongoDB
from TOOLS.redissave import Redisclient
from Func.fetchJX import FETCH
import requests
from copyheaders import headers_raw_to_dict
from lxml import etree

class ShunqiSpider:
    def __init__(self):
        self.start_url = 'https://b2b.11467.com/'
        self.headers = b"""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1616553403,1617870200; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1617870504; arp_scroll_position=400
Host: b2b.11467.com
Pragma: no-cache
Referer: https://www.11467.com/
sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-site
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"""
        self.f = FETCH()
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', "shunqiwang")
        self.r2 = Redisclient(2)
        self.r3 = Redisclient(3)
        self.area_name_list=[]
    def Get_res(self, url,headers):
        #返回可以xpath的对象的get
        # html = requests.get(url=url, headers=headers_raw_to_dict(headers))
        html = self.f.fetch(url=url, headers=headers_raw_to_dict(headers))
        res = etree.HTML(html.text)
        return res

    def get_area(self):
        res = self.Get_res(url=self.start_url,headers=self.headers)

        area_list = res.xpath('//div[@class="box sidesubcat t5"]//div[@class="boxtitle"]//following-sibling::div[@class="boxcontent"]//dl[@class="listtxt"]//dd/a/@href')
        area_name_list = res.xpath('//div[@class="box sidesubcat t5"]//div[@class="boxtitle"]//following-sibling::div[@class="boxcontent"]//dl[@class="listtxt"]//dd/a/text()')
        #"//www.11467.com/shenzhen/"
        #https://www.11467.com/shenzhen/

        for i in range(len(area_list)):
            real_url = "https:"+area_list[i]
            area_name = area_name_list[i]
            self.r2.save_category_url(area_name,real_url)
            self.area_name_list.append(area_name)
    def get_sec_category(self):
        for i in self.area_name_list:
            url = self.r2.get_category_url(i)
            res = self.Get_res(url=url,headers=self.headers)
            sec_url_list = res.xpath('//div[@id="il"]//div[@class="box huangyecity t5"]//div[@class="boxcontent"]//ul//li//dl//dt//a/@href')
            for url in sec_url_list:
                self.r2.save_page_url(i,url)
                

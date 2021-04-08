from lxml import etree
from Func.fetchJX import FETCH
from Func.client import MongoDB
from TOOLS.redissave import Redisclient
import requests


# 杭州分公司 徐浩 姓名+企业基本信息+联系方式

# {{"大类":"大类url"}:[{"小类1":"小类1url"},{"小类2":"小类2url"}.....],{},{}}


class kd8_spider:
    def __init__(self):
        self.starturl = 'http://hangzhou.qd8.com.cn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.s = FETCH()
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', "78guakao")
        self.r0 = Redisclient(0)
        self.r1 = Redisclient(1)
        self.r2 = Redisclient(2)
        self.r3 = Redisclient(3)
        self.item_dict = {}
        self.db = MongoDB('mongodb://localhost', 'cuiworkdb', 'kd8')

    def get_category(self):
        html = requests.get(url=self.starturl, headers=self.headers)
        res = etree.HTML(html.text)
        category_list = res.xpath('//div[@class="nav"]//a')[4:15]  # 除去首页，房产招聘求职
        for i in category_list:
            category_url = i.xpath('./@href')[0]
            category_url = self.starturl + category_url[1:]
            self.r0.save_page_url('一级url',category_url)

    def get_sec_category(self):
        while True:
            try:
                category_url = self.r0.get_page_url('一级url')
            except:
                break
            if category_url:
                html = requests.get(url=category_url, headers=self.headers)
                res = etree.HTML(html.text)
                sec_category_list = res.xpath('//div[@class="jzlianjie"]//a')
                for i in sec_category_list:
                    sec_category_url = i.xpath('./@href')[0]
                    sec_category_url = self.starturl + sec_category_url[1:]
                    if sec_category_url == '':
                        break
                    try:
                        self.r1.save_page_url("二级url", sec_category_url)
                    except:
                        break
            else:
                break
    def get_all_page(self):
        while True:
            try:
                print(1)
                url = self.r1.get_page_url("二级url")
                print(url)
            except:
                break
            self.r2.save_page_url("三级url", url)
            try:
                html = requests.get(url=url, headers=self.headers)
            except:
                break
            res = etree.HTML(html.text)
            while True:
                try:
                    next_page_url = res.xpath('//div[@class="paginator"]//a[contains(text(),"下一页")]/@href')[0]
                except Exception as e:
                    print(e)
                    break
                next_page_url = 'http://hangzhou.qd8.com.cn/' + next_page_url[1:]
                url = next_page_url
                self.r2.save_page_url("三级url", url)
                html = requests.get(url=url, headers=self.headers)
                res = etree.HTML(html.text)

    def get_item_url(self):
        while True:
            try:
                url = self.r2.get_page_url("三级url").decode()
                print(url)
                html = requests.get(url=url, headers=self.headers)
            except:
                break
            res = etree.HTML(html.text)
            item_url_list = res.xpath('//table//tbody//tr//td//h2//a[1]/@href')
            print(item_url_list)
            for item_url in item_url_list:
                print(item_url)
                self.r3.save_page_url('每个信息url', item_url)

    # def parse_data(self):
    #     for k in self.item_dict:
    #         for one_url in self.item_dict[k]:
    #             html = requests.get(url=one_url, headers=self.headers)
    #             res = etree.HTML(html)
    #             item_name = res.xpath('//div[@id="baselist"]//li')[0]
    #             # item_info = res.xpath('//div[@id="fangwu_view_contnet"]//text()')
    #             item_phone = res.xpath('//div[@id="yzlist"]//li[2]/text()')
    #             item = {"item_name": item_name, "item_phone": item_phone}
    #             # self.db.mongo_add(item)
    #             print(item)
    #             # //div[@id="baselist"]//li
    #             # //div[@id="yzlist"]//li

    def huangye(self):
        pass

    def run(self):
        # self.get_category()
        # self.get_sec_category()
        # self.get_all_page()
        self.get_item_url()
        # self.parse_data()


if __name__ == '__main__':
    spider = kd8_spider()
    spider.run()

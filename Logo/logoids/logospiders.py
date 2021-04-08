import requests
from lxml import etree
from mongosave import Mongoclient
from TOOLS.request_fetch import FETCH
from TOOLS.redissave import Redisclient
from time import sleep
from md5encode import id_encrypte

class Logospider:
    def __init__(self):
        self.statrurl = 'https://www.logoids.com/tags/diqu/1/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.data_demo = {'_id': '', 'category_name': '', 'brand_name': '', 'logo_url': '', }
        self.m = Mongoclient()
        # self.f=FETCH()
        self.r0 = Redisclient(0)
        self.r1 = Redisclient(1)
        self.r2 = Redisclient(2)
        self.category_list = []

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).content.decode('utf-8', 'ignore')
        # html=self.f.fetch(url)
        return html

    def parse_category_html(self, html):
        # 解析种类名和种类url

        response = etree.HTML(html)

        # //div[@class="guider"]//dl[1]//dd//ul//li//span/text() 种类名
        # //div[@class="guider"]//dl[1]//dd//ul//li//a/@href 种类url
        category_list = response.xpath('//div[@class="guider"]//dl[1]//dd//ul//li')[1:]
        for category in category_list:
            category_name = category.xpath('.//span/text()')
            category_url = category.xpath('.//a/@href')
            # 使用redis 以字符串形式储存 name 为种类名，值为url,name对url一对字符串
            self.r0.save_category_url(category_name[0], category_url[0])
            # print(self.r0.get_data(category_name[0]))
            # b'https://www.logoids.com/tags/dianqipinpai/'
            self.category_list.append(category_name[0])

    def parse_allpage(self):
        # 解析所有页数的url
        for categoryname in self.category_list:
            # 根据self.category_list从redis获取种类url

            first_page_url = self.r0.get_category_url(categoryname)
            self.r0.del_r0_item(categoryname)
            html = self.get_html(url=first_page_url)
            response = etree.HTML(html)
            self.r1.save_page_url(category_name=categoryname, page_url=first_page_url)
            while True:
                # 下一页url
                try:
                    next_page_url = \
                        response.xpath('//div[@class="pager"]/span[@class="current"]//following-sibling::a[1]/@href')[0]
                    if next_page_url:
                        # print(next_page_url)
                        self.r1.save_page_url(category_name=categoryname, page_url=next_page_url)
                        # name对全部页url，一对列表
                        html = self.get_html(url=next_page_url)
                        response = etree.HTML(html)
                    else:
                        break
                except:
                    break

    def parse_one(self):
        # 解析每一个logo的url
        for category in self.category_list:
            while True:
                try:
                    # 以种类名取出一个页的url如果还有就继续取
                    one_page_url = self.r1.get_page_url(category_name=category)
                    if one_page_url:
                        response = etree.HTML(self.get_html(one_page_url.decode()))
                        # 解析出每一页的所有item的url，列表
                        data_url_list = response.xpath('//ul[@class="list clean"]//li//div[@class="thumb"]/a/@href')
                        for one_data_url in data_url_list:
                            # 以种类为名，所有item url为列表，一对列表存储
                            self.r2.save_item_url(category_name=category, url=one_data_url)
                    else:
                        break
                except:
                    break

    def parse_data(self):
        # 解析最终数据
        for category in self.category_list:
            while True:
                try:
                    url = self.r2.get_item_url(category_name=category)
                    if url:
                        response = etree.HTML(self.get_html(url.decode()))
                        id = id_encrypte(url)
                        logocategory = category
                        logoname = response.xpath('//ul[@class="info"]//li/h1/text()')
                        logourl = response.xpath('//ul[@class="thumb-list"]//li//a/@href')

                        self.m.save_data(
                            {"_id": id, "logocategory": logocategory, "logoname": logoname[0], "logourl": logourl[0],
                             "request_url": url.decode()})
                    else:
                        break
                except Exception as e:
                    print('错误 :%s' % e)
                    break

    def run(self):
        html = self.get_html(self.statrurl)
        self.parse_category_html(html)
        self.parse_allpage()
        self.parse_one()
        self.parse_data()


if __name__ == '__main__':
    l = Logospider()
    l.run()

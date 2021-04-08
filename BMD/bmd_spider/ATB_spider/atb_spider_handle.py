from TOOLS.request_fetch import FETCH
from TOOLS.mongosave import MongoDB
from lxml import etree
from TOOLS.redissave import Redisclient


class Atb_spider:
    def __init__(self):
        # 起始url
        self.starturl = 'http://chengdu.atobo.com/'
        # 数据类型模板
        self.data_demo = {'_id': '', 'category_name': '', 'company_name': '', 'company_phone': '',
                          'company_address': ''}
        # 封装的自带代理ip池的请求
        self.f = FETCH()
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', 'BMD_atb_chengdu')
        self.r0 = Redisclient(0)
        self.r1 = Redisclient(1)
        self.r2 = Redisclient(2)
        self.r3 = Redisclient(3)
        self.category_list = []

    def parse_category_html(self):
        # 解析种类页面获取种类名称和种类url
        # 存储到redis0中，字符串类型，以种类名为名，以种类url为值
        html = self.f.fetch(self.starturl)
        response = etree.HTML(html.text)
        category_list = response.xpath('//div[@class="sidebar-category"]/ul//li/p[@class="pcategory_son"]/a')
        for category in category_list:
            category_name = category.xpath('./text()')[0]
            category_url = category.xpath('./@href')
            category_url = 'http:' + category_url[0]
            self.category_list.append(category_name)
            self.r0.save_category_url(category_name, category_url)

    def parse_more_html(self):
        # 拿到每个种类更多页url
        # 存储到redis1中，字符串类型，以种类名为名，以更多种类url为值
        for category_name in self.category_list:
            url = self.r0.get_category_url(category_name)
            html = self.f.fetch(url)
            response = etree.HTML(html.text)
            more_company_url = response.xpath('//div[@class="product-list-more"]/a/@href')[0].split('//')[1]
            self.r1.save_category_url(category_name, more_company_url)
            self.r0.del_r0_item(category_name)

    def parse_all_page(self):
        # 获取所有页的url
        # 以种类为名，以所有页url为值，所有页为列表
        for category_name in self.category_list:
            first_page_url = self.r1.get_category_url(category_name)
            # url是第一页url
            html = self.f.fetch(url=first_page_url)
            response = etree.HTML(html)
            self.r2.save_page_url(category_name, first_page_url)
            while True:
                # 下一页url
                try:
                    next_page_url = response.xpath('//div[@class="pagelist"]//span[@class="page_next page-n"]/a/@href')[
                        0]
                    if next_page_url:
                        print(next_page_url)
                        self.r2.save_page_url(category_name=category_name, page_url=next_page_url)
                        # name对全部页url，一对列表
                        html = self.f.fetch(next_page_url)
                        response = etree.HTML(html.text)
                    else:
                        break
                except:
                    break

    def parse_one_url(self):
        # 获取一页当中每个企业的url list
        for category_name in self.category_list:
            all_page_url_list=self.r2.get_page_url(category_name)
            for one_page_url in all_page_url_list:
                html = self.f.fetch(one_page_url)
                response = etree.HTML(html)
                info_list=response.xpath()

        # response = etree.HTML(html)
        # one_url_list = response.xpath(
        #     '//li[@class="product_box"]//li[@class="pp_name"]//a[@class="CompanyName"]/@href')
        # for one_url in one_url_list:
        #     one_url = "http://www.atobo.com/" + one_url

    def run(self):
        self.parse_category_html()
        self.parse_more_html()
        self.parse_all_page()


if __name__ == '__main__':
    a = Atb_spider()
    a.parse_category_html()
    a.parse_more_html()
    a.parse_all_page()

from TOOLS.request_fetch import FETCH
from TOOLS.redissave import Redisclient

# 爬虫逻辑
import requests
import re
from lxml import etree
from .address import find_address
from .tessert_atb import get_phone
from TOOLS.md5encode import phone_encrypte
from TOOLS.mongosave import MongoDB
from .ippool import proxies, get_ip
from TOOLS.request_fetch import FETCH


class Atb_spider():
    def __init__(self):
        self.starturl = 'http://bj.atobo.com/'
        # 数据类型模板
        self.data_demo = {'_id': '', 'category_name': '', 'company_name': '', 'company_phone': '',
                          'company_address': ''}
        self.f = FETCH()
        self.m = MongoDB('mongodb://10.2.1.121:17017,10.2.1.122:17017,10.2.1.123:17017', 'clues_resources',
                         'ZZ_20201214_rollback')

    def get_html(self, url):
        html = self.f.fetch(url)
        return html

    def parse_category_html(self, html):
        # 解析种类页面获取种类名称和种类url
        response = etree.HTML(html)
        category_list = response.xpath('//div[@class="sidebar-category"]/ul//li/p[@class="pcategory_son"]/a')
        for category in category_list:
            category_name = category.xpath('./text()').get()
            category_url = category.xpath('./@href').get()
            category_url = 'http:' + category_url

            # yield category_url
            yield self.parse_more_html(self.get_html(category_url), category_name=category_name)

    def parse_more_html(self, html, category_name):
        # 获取更多页选项的url
        response = etree.HTML(html)
        more_company_url = response.xpath('//div[@class="product-list-more"]/a/@href').get()

        yield self.parse_allpage(self.get_html(more_company_url), category_name=category_name)

    def parse_allpage(self, html, category_name):
        # 获取所有翻页url
        # 调用parse_one_url解析每个企业url yield出去，一页结束进入下方代码解析下一页url，再解析每个企业url
        self.parse_one_url(html, category_name=category_name)

        response = etree.HTML(html)
        one_page_url = response.xpath('//a[contains(text(),"下一页")]/@href').extract()
        if one_page_url:
            one_page_url = 'http://www.atobo.com' + one_page_url[0]
            if one_page_url != 'http://www.atobo.com#':
                yield self.parse_allpage(self.get_html(one_page_url), category_name=category_name)

    def parse_one_url(self, html, category_name):
        # 获取一页当中每个企业的url list
        response = etree.HTML(html)
        one_url_list = response.xpath(
            '//li[@class="product_box"]//li[@class="pp_name"]//a[@class="CompanyName"]/@href').extract()
        for one_url in one_url_list:
            one_url = "http://www.atobo.com/" + one_url

            yield self.parse_data(self.get_html(one_url), category_name=category_name)

    def parse_data(self, html, category_name):
        # 获取最终数据
        response = etree.HTML(html)
        try:
            # 图片规则
            company_name = response.xpath('//div[@class="company-intro"]//tr[1]/td/text()').get()
            company_address = response.xpath('//div[@class="company-intro"]//table//tr[2]').get()
            company_address = find_address(company_address)
            if not company_name:
                # 非图片规则
                company_name = response.xpath('//div[@class="company-banner"]//p[@class="t-companyname"]/text()').get()
                company_address = response.xpath('//div[@class="card-context"]//ul[2]//li[2]').get()
                company_address = find_address(company_address)
        except Exception:
            company_name = None
            company_address = None

        try:
            # 有手机号的情况
            company_phone = response.xpath('//div[@class="company-intro"]//tr/td/img/@src').extract()[1]
            company_phone = 'http:' + company_phone
            phone2 = get_phone(picurl=company_phone)
            phone = ''.join(phone2)

            if not company_phone:
                phone1 = response.xpath('//ul[4]//li[2]').get()
                pattern = re.compile("\d+", re.S)
                phone = pattern.findall(phone1)
                if not phone:
                    phone3 = response.xpath('//div[@class="company-intro"]//tr/td/img/@src').extract()[0]
                    try:
                        phone4 = 'http:' + phone3
                        phone5 = get_phone(picurl=phone4)
                        phone = ''.join(phone5)
                    except:
                        phone4 = 'http:' + phone3
                        phone5 = get_phone(picurl=phone4)
                        phone = phone5[0]

        except Exception:
            phone = None

        if company_name and phone:
            # mongo储存数据
            id = phone_encrypte(phone)
            data = self.data_demo
            data["_id"] = id
            data["categoryname"] = category_name
            data["companyname"] = company_name
            data["companyaddress"] = company_address
            data["companyphone"] = phone
            self.m.save_data(datadict=data)
            yield

    def runspider(self):
        html = self.get_html(self.starturl)
        self.parse_category_html(html)

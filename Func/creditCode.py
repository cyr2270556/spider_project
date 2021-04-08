import hashlib
import json
import time
from urllib import parse

from Func.Parse import FETCH
from Func.Tyc3 import FETCH1
from lxml import etree
from Func.client import MongoDB

s = FETCH()
s1 = FETCH1()
db = MongoDB('172.16.74.249:27017', 'creditCode', 'KJ')


class GetCode(object):
    def __init__(self):
        self.item = {}
        self.item1 = {}  # 信用中国
        self.item2 = {}  # 天眼查
        self.item3 = {}
        self.code = {'200': '请求成功', '203': '请求失败，please重试',
                     '204': '所查询公司不精确或不存在'}

    def Mongo(self, Item):
        db.mongo_add(Item)

    # 百度企业信用基本信息
    def BaiduCreit(self, company_name):
        print('进入百度信用')
        res1 = s.fetch('https://xin.baidu.com/s?q={}&t=0'.format(parse.quote(company_name)), method='GET')
        if res1:
            tree1 = etree.HTML(res1.text)
            href_list = tree1.xpath('//a[@class="zx-list-item-url"]/@href')
            if len(href_list) != 0:
                details_href = 'https://xin.baidu.com' + href_list[0]
                company = tree1.xpath('//a[@class="zx-list-item-url"]/@title')[0]
                res = s.fetch(details_href, method='GET')
                tree = etree.HTML(res.text)
                # 统一社会信用代码
                try:
                    Baidu_code = tree.xpath(
                        '//td[contains(text(),"统一社会信用代码")]/following-sibling::td[1]/text()')[0]
                    if Baidu_code == '-':
                        self.SkyCreit(company_name)
                        self.item.clear()
                    elif company_name != company:
                        self.item['companyName'] = company_name
                        self.item['code'] = '204'
                        self.item['Tips'] = self.code['204']
                    else:
                        self.item['companyName'] = company_name
                        self.item['creditCode'] = Baidu_code
                        self.item['code'] = '200'
                        self.item['Tips'] = self.code['200']
                except:
                    self.item['companyName'] = company_name
                    self.item['code'] = '204'
                    self.item['Tips'] = self.code['204']


            else:
                self.SkyCreit(company_name)
        else:
            self.item['companyName'] = company_name
            self.item['code'] = '203'
            self.item['Tips'] = self.code['203']

    def SkyCreit(self, company_name):
        print('进入天眼查')
        # 搜索：公司列表
        company_url = 'https://api9.tianyancha.com/services/v3/search/sNorV4/{}?sortType=0&pageSize=10&pageNum=1'.format(
            parse.quote(company_name))
        res = s1.fetch1(company_url)
        if res:
            cont = json.loads(res.text)['data']['companyList']
            if len(cont) != 0:
                cid = cont[0]['id']
                company = cont[0]['name'].replace('</em>', '').replace('<em>', '')
                url = 'https://api9.tianyancha.com/services/v3/t/details/appComIcV4/{}?pageSize=1000'.format(cid)
                res1 = s1.fetch1(url)
                content = json.loads(res1.text)['data']['baseInfo']
                # 统一社会信用代码
                self.item2['companyName'] = company_name
                if company_name != company:
                    self.item2['code'] = '204'
                    self.item2['Tips'] = self.code['204']
                else:
                    self.item2['creditCode'] = content['creditCode']
                    self.item2['code'] = '200'
                    self.item2['Tips'] = self.code['200']
        else:
            self.item2['companyName'] = company_name
            self.item2['code'] = '203'
            self.item2['Tips'] = self.code['203']

    def XinyongChina(self, company_name):
        print('进入信用中国')
        res = s.fetch(
            'https://public.creditchina.gov.cn/private-api/catalogSearch?keyword={}&scenes=defaultscenario&tableName=credit_xyzx_tyshxydm&searchState=2&entityType=1,2,4,5,6,7,8&page=1&pageSize=10'.format(
                parse.quote(company_name)))
        content = json.loads(res.text)['data']
        if res.status_code != 200:
            content['list'] = []
        else:
            content = content
        self.item1['companyName'] = company_name
        if len(content['list']) != 0:
            company = content['list'][0]['jgmc']
            if company_name != company:
                self.item1['code'] = '204'
                self.item1['Tips'] = self.code['204']
            else:
                self.item1['creditCode'] = content['list'][0]['tyshxydm']
                self.item1['code'] = '200'
                self.item1['Tips'] = self.code['200']

        else:
            self.BaiduCreit(company_name)
            if self.item == {}:
                try:
                    self.item3['_id'] = hashlib.md5(str(time.time()).encode(encoding='utf-8')).hexdigest()
                    self.item3['companyName'] = self.item2['companyName']
                    self.item3['Tips'] = self.item2['Tips']
                    # 接口使用时间
                    self.item3['usage_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    self.Mongo(self.item3)
                    return self.item2
                except:
                    return self.code['204']
            else:
                try:
                    self.item3['_id'] = hashlib.md5(str(time.time()).encode(encoding='utf-8')).hexdigest()
                    self.item3['companyName'] = self.item['companyName']
                    self.item3['Tips'] = self.item['Tips']
                    # 接口使用时间
                    self.item3['usage_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                    self.Mongo(self.item3)
                    return self.item
                except:
                    return self.code['204']
        try:
            self.item3['_id'] = hashlib.md5(str(time.time()).encode(encoding='utf-8')).hexdigest()
            self.item3['companyName'] = self.item1['companyName']
            self.item3['Tips'] = self.item1['Tips']
            # 接口使用时间
            self.item3['usage_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            self.Mongo(self.item3)
            return self.item1
        except:
            return self.code['204']


a = GetCode()
v = a.XinyongChina('成都怆业之家企业管理有限公司')
print(v)


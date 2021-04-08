# import re
# from concurrent.futures.thread import ThreadPoolExecutor
# from urllib import parse

# import pymysql
#
# from Func.Parse import FETCH
#
# from Func.Redis import REDIS
# from Func.conf import *
# import json
#
# redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=qcc1)
# s = FETCH()


# class get_json(object):
#     def __init__(self):
#         self.item = {}
#         self.item1 = {}
#         self.dic = {'200': '数据抓取成功', '201': '未找到匹配的公司名', '202': '网站信息抓取失败', '203': '抓取成功，信息存储失败'}
#         self.code200 = '200'
#         self.code201 = '201'
#         self.code202 = '202'
#         self.code203 = '203'
#
#     def save_article_date(self,items):
#         conn = pymysql.Connect(host='192.168.254.144',
#                                port=3306,
#                                db='baidu_company',
#                                user='root',
#                                password='root',
#                                charset='utf8mb4')
#         cursor = conn.cursor()
#         # aid唯一标识符
#         cursor.execute("select companyName from company_info where companyName='%s'" % items['companyName'])
#         results = cursor.fetchall()
#         try:
#             if not results:
#                 sql = 'insert into `company_info`(creditCode,companyName,organizationCode,registerNum,businessState,industry,legalMan,registerMoney,registerTime,registOrgan,confirmTime,businessTimeout,companyType,registerAddress,businessScope,personnelScale,insuredPersons,usedName,operation,webSource) values("%s", "%s", "%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
#                       % (items['creditCode'],items['companyName'],items['organizationCode'],items['registerNum'],items['businessState'],items['industry'],items['legalMan'],items['registerMoney'],items['registerTime'],items['registOrgan'],items['confirmTime'],items['businessTimeout'],items['companyType'],items['registerAddress'],items['businessScope'],items['personnelScale'],items['insuredPersons'],items['usedName'],items['operation'],items['webSource'])
#                 try:
#                     cursor.execute(sql)
#                     conn.commit()
#                     print('插入公司名----%s' % items['companyName'])
#                     return self.code200
#                 except Exception as e:
#                     print(e)
#                     conn.rollback()
#
#             else:
#                 print('该%s已存在数据库' % items['companyName'])
#                 return self.code200
#         except Exception as e:
#             if e:
#                 return self.code203
#
#         cursor.close()
#         conn.close()
#
#     # 百度企业信用基本信息
#     def get_companydetails(self, company_name):
#         res1 = s.fetch('https://xin.baidu.com/s?q={}&t=0'.format(parse.quote(company_name)))
#         details_href = 'https://xin.baidu.com' + res1.html.xpath('//a[@class="zx-list-item-url"]/@href')[0]
#         company = res1.html.xpath('//a[@class="zx-list-item-url"]/@title')[0]
#         res = s.fetch(details_href)
#         # 统一社会信用代码
#         self.item['creditCode'] = res.html.xpath('//td[contains(text(),"统一社会信用代码")]/following-sibling::td[1]/text()', first=True)
#         # 客户公司注册时间
#         self.item['registerTime'] = res.html.xpath(
#             '//*[@class="zx-detail-basic-table"]//td[contains(text(),"成立日期")]/following-sibling::td[1]/text()',
#             first=True)
#         # 客户公司注册金额 registerMoney
#         self.item['registerMoney'] = res.html.xpath('//td[contains(text(),"注册资本")]/following-sibling::td[1]/text()', first=True)
#         # 客户所属行业
#         self.item['industry'] = res.html.xpath('//td[contains(text(),"所属行业")]/following-sibling::td[1]/text()', first=True)
#         # 客户公司状态：正常/注销
#         self.item['businessState'] = res.html.xpath('//td[contains(text(),"经营状态")]/following-sibling::td[1]/text()', first=True)
#         # 组织机构代码
#         self.item['organizationCode'] = res.html.xpath('//td[contains(text(),"组织机构代码")]/following-sibling::td[1]/text()', first=True)
#         # 工商注册号
#         self.item['registerNum'] = res.html.xpath('//td[contains(text(),"工商注册号")]/following-sibling::td[1]/text()', first=True)
#         # 法定代表人
#         self.item['legalMan'] = res.html.xpath('//td[contains(text(),"法定代表人")]/following-sibling::td[1]/text()', first=True)
#         # 登记机关
#         self.item['registOrgan'] = res.html.xpath('//td[contains(text(),"登记机关")]/following-sibling::td[1]/text()', first=True)
#         # 核准日期
#         self.item['confirmTime'] = res.html.xpath('//*[@class="zx-detail-basic-table"]//td[contains(text(),"审核/年检日期")]/following-sibling::td[1]/text()', first=True)
#         # 营业期限
#         self.item['businessTimeout'] = res.html.xpath('//*[@class="zx-detail-basic-table"]//td[contains(text(),"营业期限")]/following-sibling::td[1]/text()', first=True)
#         # 企业类型
#         self.item['companyType'] = res.html.xpath('//*[@class="zx-detail-basic-table"]//td[contains(text(),"企业类型")]/following-sibling::td[1]/text()', first=True)
#         # 企业地址
#         self.item['registerAddress'] = res.html.xpath('//*[@class="zx-detail-basic-table"]//td[contains(text(),"注册地址")]/following-sibling::td[1]/text()', first=True)
#         # 经营范围
#         self.item['businessScope'] = res.html.xpath('//td[contains(text(),"经营范围")]/following-sibling::td[1]//@data-content',first=True)
#         # 人员规模
#         self.item['personnelScale'] = None
#         # 参保人数
#         self.item['insuredPersons'] = None
#         # 曾用名
#         self.item['usedName'] = res.html.xpath('//td[contains(text(),"曾用名")]/following-sibling::td[1]/text()', first=True)
#         # 经营方式
#         self.item['operation'] = None
#         # 来源网站
#         self.item['webSource'] = 'https://xin.baidu.com/'
#         self.item['companyName'] = company_name
#         # print(self.item)
#         return self.item
#
#         # # code 200
#         # if company_name == company and len(self.item) > 2:
#         #     code = self.save_article_date(self.item)
#         #     self.item1['code'] = code
#         #     self.item1['message'] = self.dic[self.item1['code']]
#         #     self.item1['data'] = {'data.db': 'baidu_company', 'data.table': 'company_info', 'webSource': self.item['webSource']}
#         #     return self.item1
#         # # code 202
#         # elif len(self.item) == 2:
#         #     self.item1['code'] = self.code202
#         #     self.item1['message'] = self.dic[self.code202]
#         #     self.item1['data'] = None
#         #     return self.item1
#         # # code = 201
#         # elif company_name != company and len(self.item) > 2:
#         #     self.item1['code'] = self.code201
#         #     self.item1['message'] = self.dic[self.code201]
#         #     self.item1['data'] = None
#         #     return self.item1
#         # # code = 203
#         # elif company_name == company and len(self.item) > 2:
#         #     code = self.save_article_date(self.item)
#         #     self.item1['code'] = code
#         #     self.item1['message'] = self.dic[self.item1['code']]
#         #     self.item1['data'] = None
#         #     return self.item1
#         # else:
#         #     return '程序错误'


import hashlib
import json
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from urllib import parse

from Func.Parse import FETCH
from Func.client import MongoDB
from Func.conf import *
from Func.Redis import REDIS

s = FETCH()
db1 = MongoDB('172.16.74.249:27017', 'db_reptile_company', 'company_details')


class get_json(object):
    def __init__(self):
        self.db = MongoDB('172.16.74.249:27017', 'db_reptile_company', 'company_name')
        self.redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=RedisDB)
        self.item = {}

    # mongdb--redeis
    def transfer(self):
        dd = self.db.mongo_find({})
        for i in dd:
            item = {}
            item['_id'] = i['_id']
            item['company_name'] = i['company_name']
            b = self.redis.add('coampanylidt', json.dumps(item))
            print('存入成功', b, item)

    # 百度企业信用基本信息
    def get_companydetails(self, company_name):
        res1 = s.fetch('https://xin.baidu.com/s?q={}&t=0'.format(parse.quote(company_name)))
        href_list = re.findall(r'{"pid":"(\S+)","entName":', res1.text)
        if len(href_list) != 0:
            details_href = 'https://xin.baidu.com//detail//compinfo?pid=' + href_list[0]
            # company = res1.html.xpath('//a[@class="zx-list-item-url"]/@title')[0]
            print(details_href)
            res = s.fetch(details_href)
            # print(res.text)
            exit()
            # 统一社会信用代码
            self.item['credit_code'] = res.html.xpath(
                '//td[contains(text(),"统一社会信用代码")]/following-sibling::td[1]/text()',
                first=True)
            # 客户公司注册时间
            self.item['register_time'] = res.html.xpath(
                '//*[@class="zx-detail-basic-table"]//td[contains(text(),"成立日期")]/following-sibling::td[1]/text()',
                first=True)
            # 客户公司注册金额 registerMoney
            self.item['register_money'] = res.html.xpath(
                '//td[contains(text(),"注册资本")]/following-sibling::td[1]/text()',
                first=True)
            # 客户所属行业
            self.item['industry'] = res.html.xpath('//td[contains(text(),"所属行业")]/following-sibling::td[1]/text()',
                                                   first=True)
            # 客户公司状态：正常/注销
            self.item['business_state'] = res.html.xpath(
                '//td[contains(text(),"经营状态")]/following-sibling::td[1]/text()',
                first=True)
            # 组织机构代码
            self.item['organization_code'] = res.html.xpath(
                '//td[contains(text(),"组织机构代码")]/following-sibling::td[1]/text()', first=True)
            # 工商注册号
            self.item['register_num'] = res.html.xpath('//td[contains(text(),"工商注册号")]/following-sibling::td[1]/text()',
                                                       first=True)
            # 法定代表人
            self.item['legal_man'] = res.html.xpath('//td[contains(text(),"法定代表人")]/following-sibling::td[1]/text()',
                                                    first=True)
            # 登记机关
            self.item['regist_organ'] = res.html.xpath('//td[contains(text(),"登记机关")]/following-sibling::td[1]/text()',
                                                       first=True)
            # 核准日期
            self.item['confirmtime'] = res.html.xpath(
                '//*[@class="zx-detail-basic-table"]//td[contains(text(),"审核/年检日期")]/following-sibling::td[1]/text()',
                first=True)
            # 营业期限
            self.item['business_timeout'] = res.html.xpath(
                '//*[@class="zx-detail-basic-table"]//td[contains(text(),"营业期限")]/following-sibling::td[1]/text()',
                first=True)
            # 企业类型
            self.item['register_address'] = res.html.xpath(
                '//*[@class="zx-detail-basic-table"]//td[contains(text(),"企业类型")]/following-sibling::td[1]/text()',
                first=True)
            # 企业地址
            self.item['registerAddress'] = res.html.xpath(
                '//*[@class="zx-detail-basic-table"]//td[contains(text(),"注册地址")]/following-sibling::td[1]/text()',
                first=True)
            # 经营范围
            self.item['business_scope'] = res.html.xpath(
                '//td[contains(text(),"经营范围")]/following-sibling::td[1]//@data-content', first=True)

            self.item['usedName'] = res.html.xpath('//td[contains(text(),"曾用名")]/following-sibling::td[1]/text()',
                                                   first=True)
            # 经营方式
            # self.item['operation'] = None
            # 来源网站
            self.item['web_source'] = 'https://xin.baidu.com/'
            # 公司名
            self.item['company_name'] = company_name
            # 来源网址
            self.item['company_url'] = details_href
            self.item['_id'] = hashlib.md5((company_name).encode(encoding='utf-8')).hexdigest()
            self.item['web_update_time'] = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
            # print(self.item)
            # return self.item
            # code 201
            if company_name != company and len(self.item) > 4:
                self.db.mong_find_one_update({"_id": self.item['_id']}, {"flag": "公司名有问题"})
                return '公司名有问题 --- %s' % self.item['company_name']
            else:
                db1.mongo_add(self.item)
                return '%s 插入成功 !!!!' % self.item['company_name']

        else:
            _id = hashlib.md5((company_name).encode(encoding='utf-8')).hexdigest()
            self.db.mong_find_one_update({"_id": _id}, {"flag": "未找到匹配的公司名"})
            return '未找到匹配的公司名---%s' % company_name

#
if __name__ == '__main__':
    v = get_json()
    # v.main()
    company_name = '阿里巴巴(中国)网络技术有限公司'
    v.get_companydetails(company_name)

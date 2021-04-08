import re
from concurrent.futures.thread import ThreadPoolExecutor
from urllib import parse

import pymysql

from Func.Parse import FETCH

from Func.Redis import REDIS
from Func.conf import *
import json

redis = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=qcc1)
s = FETCH()


class get_json(object):
    def __init__(self):
        self.item = {}
        self.item1 = {}
        self.dic = {'200': '数据抓取成功', '201': '未找到匹配的公司名', '202': '网站信息抓取失败', '203': '抓取成功，信息存储失败'}
        self.code200 = '200'
        self.code201 = '201'
        self.code202 = '202'
        self.code203 = '203'

    def save_article_date(self,items):
        conn = pymysql.Connect(host='192.168.254.144',
                               port=3306,
                               db='baidu_company',
                               user='root',
                               password='root',
                               charset='utf8mb4')
        cursor = conn.cursor()
        # aid唯一标识符
        cursor.execute("select ruInCause from company_abnormal where ruInCause='%s'" % items['ruInCause'])
        results = cursor.fetchall()
        try:
            if not results:
                sql = 'insert into `company_abnormal`(companyName,ruInTime,ruSection,ruInCause,ruOutTime,ruOutCause,chuSection,abnormalInfoCount,webSource) values("%s", "%s", "%s", "%s","%s","%s","%s","%s","%s")' \
                      % (items['companyName'],items['ruInTime'],items['ruSection'],items['ruInCause'],items['ruOutTime'],items['ruOutCause'],items['chuSection'],items['abnormalInfoCount'],items['webSource'])
                try:
                    cursor.execute(sql)
                    conn.commit()
                    print('插入公司名----%s' % items['companyName'])
                    return self.code200
                except Exception as e:
                    print(e)
                    conn.rollback()

            else:
                print('该%s已存在数据库' % items['companyName'])
                return self.code200
        except Exception as e:
            if e:
                return self.code203

        cursor.close()
        conn.close()

    def get_abnormal(self, company_name):
        global a
        res1 = s.fetch('https://xin.baidu.com/s?q={}&t=0'.format(parse.quote(company_name)))
        details_href = 'https://xin.baidu.com' + res1.html.xpath('//a[@class="zx-list-item-url"]/@href')[0]
        company = res1.html.xpath('//a[@class="zx-list-item-url"]/@title')[0]
        res = s.fetch(details_href)
        pid = re.findall(r'result":{"pid":"(\d+)","defTags"', res.text)[0]
        wenshu_url = 'https://xin.baidu.com/detail/abnormalAjax?pid={}&p=1'.format(pid)
        response = s.fetch(wenshu_url)
        content = json.loads(response.text.encode('utf8').decode('unicode_escape'))['data']
        if len(content['list']) != 0:
            for i in content['list']:
                # 公司名
                self.item['companyName'] = company
                # 列入日期
                self.item['ruInTime'] = i['enterDate']
                # 列入决定机关
                self.item['ruSection'] = i['authority']
                # 列入经营异常名录原因
                self.item['ruInCause'] = i['enterReason']
                # 移出日期
                self.item['ruOutTime'] = i['leaveDate']
                # 移出经营异常名录原因
                self.item['ruOutCause'] = i['leaveReason']
                # 移出决定机关
                self.item['chuSection'] = i['leaveAuthority']
                # 经营异常计数
                self.item['abnormalInfoCount'] = content['totalNum']
                # 来源网站
                self.item['webSource'] = 'https://xin.baidu.com/'
                print(self.item)

                a = self.fun1(company_name, company)
            return a
        else:
            return '该公司无经营异常信息'

    def fun1(self, company_name,company):
        if company_name == company and len(self.item) > 2:
            code = self.save_article_date(self.item)
            self.item1['code'] = code
            self.item1['message'] = self.dic[self.item1['code']]
            self.item1['data'] = {'data.db': 'baidu_company', 'data.table': 'company_abnormal', 'webSource': self.item['webSource']}
            return self.item1
        # code 202
        elif len(self.item) == 2:
            self.item1['code'] = self.code202
            self.item1['message'] = self.dic[self.code202]
            self.item1['data'] = None
            return self.item1
        # code = 201
        elif company_name != company and len(self.item) > 2:
            self.item1['code'] = self.code201
            self.item1['message'] = self.dic[self.code201]
            self.item1['data'] = None
            return self.item1
        # code = 203
        elif company_name == company and len(self.item) > 2:
            code = self.save_article_date(self.item)
            self.item1['code'] = code
            self.item1['message'] = self.dic[self.item1['code']]
            self.item1['data'] = None
            return self.item1
        else:
            return '程序错误'


b = get_json()
b.get_abnormal('河南捷弘餐饮服务有限公司')
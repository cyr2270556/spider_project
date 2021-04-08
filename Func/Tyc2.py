from urllib import parse
import json
import time
import pymysql
from Func.tycfetch import FETCH


class get_Tycjson(object):
    def __init__(self):
        self.item = {}
        self.item1 = {}
        self.dic = {'200': '数据抓取成功', '201': '未找到匹配的公司名', '202': '网站信息抓取失败', '203': '抓取成功，信息存储失败'}
        self.code200 = '200'
        self.code201 = '201'
        self.code202 = '202'
        self.code203 = '203'

    def save_article_date(self, items):
        conn = pymysql.Connect(host='192.168.254.144',
                               port=3306,
                               db='baidu_company',
                               user='root',
                               password='root',
                               charset='utf8mb4')
        cursor = conn.cursor()
        # aid唯一标识符
        cursor.execute("select companyName from company_info where companyName='%s'" % items['companyName'])
        results = cursor.fetchall()
        try:
            if not results:
                sql = 'insert into `company_info`(creditCode,companyName,organizationCode,registerNum,businessState,industry,legalMan,registerMoney,registerTime,registOrgan,confirmTime,businessTimeout,companyType,registerAddress,businessScope,personnelScale,insuredPersons,usedName,operation,webSource) values("%s", "%s", "%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
                      % (items['creditCode'], items['companyName'], items['organizationCode'], items['registerNum'],
                         items['businessState'], items['industry'], items['legalMan'], items['registerMoney'],
                         items['registerTime'], items['registOrgan'], items['confirmTime'], items['businessTimeout'],
                         items['companyType'], items['registerAddress'], items['businessScope'],
                         items['personnelScale'], items['insuredPersons'], items['usedName'], items['operation'],
                         items['webSource'])
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

    def get_compnayInfo(self, company_name):
        s = FETCH()
        # 搜索：公司列表
        company_url = 'https://api9.tianyancha.com/services/v3/search/sNorV4/{}?sortType=0&pageSize=10&pageNum=1'.format(
            parse.quote(company_name))
        res = s.fetch(company_url)
        cont = json.loads(res.text)['data']['companyList']
        cid = cont[0]['id']
        company = cont[0]['name'].replace('</em>', '').replace('<em>', '')
        print(company)
        # exit()
        # 工商信息链接
        # url = 'https://api9.tianyancha.com/services/v3/t/details/appComIcV4/1698375?pageSize=1000'
        url = 'https://api9.tianyancha.com/services/v3/t/details/appComIcV4/{}?pageSize=1000'.format(cid)
        res1 = s.fetch(url)
        content = json.loads(res1.text)['data']['baseInfo']
        # 统一社会信用代码
        self.item['companyName'] = company
        try:
            self.item['creditCode'] = content['creditCode']
        except:
            self.item['creditCode'] = '-'
        # 组织机构代码
        try:
            self.item['organizationCode'] = content['orgNumber']
        except:
            self.item['organizationCode'] = '-'
        # 工商注册号
        try:
            self.item['registerNum'] = content['regNumber']
        except:
            self.item['registerNum'] = '-'
        # 经营状态
        try:
            self.item['businessState'] = content['regStatus']
        except:
            self.item['businessState'] = '-'
        # 所属行业
        try:
            self.item['industry'] = content['industry']
        except:
            self.item['industry'] = '-'
        # 法定代表人
        try:
            self.item['legalMan'] = content['legalPersonName']
        except:
            self.item['legalMan'] = '-'
        # 注册资本
        try:
            self.item['registerMoney'] = content['regCapital']
        except:
            self.item['registerMoney'] = '-'
        # 成立日期
        try:
            self.item['registerTime'] = content['estiblishTime']
        except:
            self.item['registerTime'] = '-'
        # 登记机关
        try:
            self.item['registOrgan'] = content['regInstitute']
        except:
            self.item['registOrgan'] = '-'
        # 核准日期
        try:
            self.item['confirmTime'] = content['approvedTime']
        except:
            self.item['confirmTime'] = '-'
        # 营业期限
        try:
            a = time.strftime('%Y-%m-%d', time.localtime(content['estiblishTime'] // 1000))
        except:
            a = '-'
        try:
            b = time.strftime('%Y-%m-%d', time.localtime(content['toTime'] // 1000))
        except:
            b = '-'
        self.item['businessTimeout'] = a + '至' + b
        # 企业类型
        try:
            self.item['companyType'] = content['companyOrgType']
        except:
            self.item['companyType'] = '-'
        # 企业地址
        try:
            self.item['registerAddress'] = content['regLocation']
        except:
            self.item['registerAddress'] = '-'
        # 经营范围
        try:
            self.item['businessScope'] = content['businessScope']
        except:
            self.item['businessScope'] = '-'
        # 人员规模content['toTime']
        try:
            self.item['personnelScale'] = content['staffNumRange']
        except:
            self.item['personnelScale'] = '-'
        # 参保人数
        try:
            self.item['insuredPersons'] = content['socialStaffNum']
        except:
            self.item['insuredPersons'] = '-'
        # 曾用名
        self.item['usedName'] = None
        # 经营方式
        self.item['operation'] = None
        # 来源网站
        self.item['webSource'] = 'https://www.tianyancha.com/'
        # return self.item

        # code 200
        if company_name == company and len(self.item) > 2:
            return self.item
            # code = self.save_article_date(self.item)
            # self.item1['code'] = code
            # self.item1['message'] = self.dic[self.item1['code']]
            # self.item1['data'] = {'data.db': 'baidu_company', 'data.table': 'company_info',
            #                       'webSource': self.item['webSource']}
            # return self.item1
        # code 202
        elif len(self.item) == 2:
            self.item1['err_msg'] = '实时查询结果失败，请点击重新尝试'
            # self.item1['code'] = self.code202
            # self.item1['message'] = self.dic[self.code202]
            # self.item1['data'] = None
            return self.item1
        # code = 201
        elif company_name != company and len(self.item) > 2:
            self.item1['err_msg'] = '未找到符合条件的查询结果，请更改关键词重新查询'
            # self.item1['code'] = self.code201
            # self.item1['message'] = self.dic[self.code201]
            # self.item1['data'] = None
            return self.item1
        # code = 203
        # elif company_name == company and len(self.item) > 2:
        #     self.item1['err_msg'] = '未找到符合条件的查询结果，请更改关键词重新查询'
        #     # code = self.save_article_date(self.item)
        #     # self.item1['code'] = code
        #     # self.item1['message'] = self.dic[self.item1['code']]
        #     # self.item1['data'] = None
        #     return self.item1
        else:
            return '程序错误'


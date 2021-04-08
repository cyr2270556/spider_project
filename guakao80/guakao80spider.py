import requests
from lxml import etree
from Func.fetchJX import FETCH
from Func.client import MongoDB
from TOOLS.redissave import Redisclient
import re
from TOOLS.md5encode import md5encryption
from time import sleep
import random
# 北京分公司	资质事业部	李丹 80挂靠网	http://www.80guakao.com/	姓名+电话+证书专业


class Gkspider:
    def __init__(self):
        self.starturl = 'http://www.80guakao.com/shengfen/hb/zhaopinxinxi/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.f = FETCH()
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', "80guakao_hb")
        self.r0 = Redisclient(0)
        self.r1 = Redisclient(1)
        self.r2 = Redisclient(2)
        self.r3 = Redisclient(3)
        self.category_name_list = []
        self.sec_category_dict = {}
        self.headers_forpage = {
            "Host":"www.80guakao.com",
            "Connection":"keep-alive",
            "Pragma":"no-cache",
            "Cache-Control":"no-cache",
            "User-Agent":"Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.111Safari / 537.36",
            "Accept":"*/*",
            "Referer":"http://www.80guakao.com/shengfen/hb/",
            "Accept-Encoding":"gzip,deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cookie":"",
        }

    def get_category(self):
        html = self.f.fetch(url=self.starturl, headers=self.headers,method='get')
        # html = requests.get(url=self.starturl, headers=self.headers)
        sleep(random.randint(0, 1))
        res = etree.HTML(html.text)
        # print(html.text)

        # category_url_list = res.xpath('//div[@class="content"]//div//a')
        # # if len(category_url_list) > 19:
        # category_url_list = res.xpath('//div[@class="inner"][1]//ul[1]//a')
        category_url_list = res.xpath('//div[@class="categories"]//ul//li[1]//dd[1]//a')
        for i in category_url_list:
            category_name = i.xpath('./text()')[0]
            category_url = i.xpath('./@href')[0]
            category_url = category_url.replace('m.', 'www.')
            if category_name != "不限":
                self.r0.save_category_url(category_name, category_url)
                self.category_name_list.append(category_name)

    def get_sec_category(self):
        for category_name in self.category_name_list:

            url = self.r0.get_category_url(category_name)
            # html = self.f.fetch(url=url,headers=self.headers,method='get')
            html = requests.get(url=url, headers=self.headers_forpage)
            sleep(random.randint(0, 1))
            res = etree.HTML(html.text)

            sec_category_list = res.xpath('//div[@class="content"]//div//a')
            # sec_category_list = res.xpath('//div[@class="inner"][1]//ul//a')

            for i in sec_category_list:
                sec_category_name = i.xpath('./text()')[0]
                sec_category_url = i.xpath('./@href')[0]
                sec_category_url = sec_category_url.replace('m.', 'www.')
                if sec_category_name != '不限':
                    print(sec_category_name)
                    self.r1.save_one_dict(category_name, sec_category_name, sec_category_url)

    def get_all_page(self):
        for category in self.category_name_list:
            sec_category_list = self.r1.get_keys(category)

            for sec_category_name, url in sec_category_list.items():
                # html = self.f.fetch(url=url.decode(),headers=self.headers_forpage,method='get')
                html = requests.get(url=url.decode(), headers=self.headers_forpage)
                sleep(random.randint(0, 1))
                res = etree.HTML(html.text)
                self.r2.save_page_url(category + ":" + sec_category_name.decode(), url.decode())
                while True:
                    try:
                        next_page = res.xpath('//div[@class="pagination2"]//a[contains(text(),"下一页")]/@href')[0]
                    except:
                        break
                    if not next_page:
                        break

                    self.r2.save_page_url(category + ":" + sec_category_name.decode(), next_page)
                    html_next = self.f.fetch(url=next_page, headers=self.headers_forpage,method='get')
                    # html_next = requests.get(url=next_page, headers=self.headers_forpage)
                    sleep(random.randint(0,1))
                    res = etree.HTML(html_next.text)

    def get_item_url(self):
        for category in self.category_name_list:
            sec_category_list = self.r1.get_keys(category)
            for sec_category_name in sec_category_list:
                while True:
                    try:
                        url = self.r2.get_page_url(category + ":" + sec_category_name.decode())
                        # html = self.f.fetch(url=url, headers=self.headers,method='get')
                        html = requests.get(url=url,headers=self.headers_forpage)
                        sleep(random.randint(1,2))
                        res = etree.HTML(html.text)
                    except Exception as e:
                        print('error:' , e)
                        break
                    # item_list = res.xpath('//li[@class="Tz"]//child::*/a/@href')
                    item_list = res.xpath('/html/body/div[7]/div[5]/div/div[6]/div[4]/div[3]/ul/div/span[1]/a/@href')

                    for item_url in item_list:
                        # if 'tel' not in item_url:
                        #     url = item_url.replace('m.', 'www.') #每个数据url
                        if 'http' not in item_url:
                            item_url = 'http://www.80guakao.com/' + item_url
                        self.r3.save_item_url(category+':'+sec_category_name.decode(), item_url)


    def get_info(self):
        # print(res.xpath('//ul[@class="attr_info"]//li//span[@class="attrVal"]/text()')[0]) #公司名
        # print(res.xpath('//ul[@class="attr_info bottom"]//li//span[@class="attrVal"]//a/text()')[0]) #电话
        # print(res.xpath('//ul[@class="attr_info bottom"]//li//span[@class="attrVal"]/text()')[0])  # 姓名
        for category in self.category_name_list:
            sec_category_list = self.r1.get_keys(category)
            for sec_category_name in sec_category_list:
                while True:
                    try:
                        url = self.r3.get_item_url(category + ":" + sec_category_name.decode())

                        html = requests.get(url=url.decode(), headers=self.headers_forpage)
                        sleep(random.randint(0 ,1))
                        if html.status_code != 200:
                            html = self.f.fetch(url=url.decode(), headers=self.headers_forpage, method='get')
                            sleep(random.randint(0,1))
                        res = etree.HTML(html.text)

                    except:
                        break
                    item = {}
                    # try:
                    #     company_name = res.xpath('//ul[@class="attr_info"]//li//span[@class="attrVal"][1]/text()')[0]
                    # except:
                    try:
                        company_name = res.xpath('//div[@class="zhaopiner"]//li//span[contains(text(),"公司名称")]/parent::li/text()')[0]

                    except:
                        company_name = 'None'

                    # try:
                    #     contact_people = res.xpath('//ul[@class="attr_info bottom"]//li[2]//span[@class="attrVal"]/text()')[0]
                    #     contact_people = contact_people.replace(r'\xa0\xa0','')
                    #
                    # except:
                    contact_people = res.xpath('//ul[@class="contacter"]//li//font/text()')[0]


                    # try:
                    #     perf_request = res.xpath('//div[@class="zhaopiner"]//li//span[contains(text(),"专业要求")]/parent::li/text()')[0]
                    # except:
                    #
                    #     perf_request = res.xpath('//ul[@class="attr_info"]//li//span[@class="attrVal"][11]//text()')[0]
                    #

                    # try:
                    #     phone = res.xpath('//ul[@class="attr_info"]//li//span[@class="attrVal"][11]//a/text()')[0]
                    #     if phone == []:
                    #         raise  Exception
                    # except:

                    # try:
                    phone_url_re = res.xpath('//ul[@class="contacter"]//li[@class="qqbm"]/a/@onclick')[0]

                    par = re.compile("'.*?'")
                    phone_url = re.findall(par, phone_url_re)[1].replace("'", "")  # 电话号码url

                    if type(phone_url) == str:
                        html = requests.get(url=phone_url, headers=self.headers_forpage)
                    else:
                        html = requests.get(url=phone_url.decode(), headers=self.headers_forpage)
                        sleep(random.randint(0,1))
                    res = etree.HTML(html.text)
                    phone = res.xpath('//div[@class="number"]//span[@class="num"]/text()')[0]
                    # except:
                    #     phone = "None"


                    item['companyCity'] = '宜昌'
                    item['companyProvince'] = '湖北省'
                    item['code'] = 'BUS_YT_ZZ'
                    item['name'] = '资质'
                    item['busCode'] = ''
                    item['webUrl'] = '无'
                    item['orgId'] = ''
                    # 部门ID 字符串
                    item['deptId'] = ''
                    # 中心ID 字符串
                    item['centreId'] = ''
                    # item["first_category"] = category
                    # item["sec_category"] = sec_category_name.decode()
                    item["companyName"] = company_name
                    item["outName"] = contact_people
                    item["resourceRemark"] = category+":"+sec_category_name.decode()
                    item["companyTel"] = phone.strip()
                    if len(contact_people) == 11:
                        item["companyTel"] = contact_people
                    item["ibossNum"] = None
                    item['isDir'] = 0
                    item['isShare'] = 0
                    item["_id"] = md5encryption(item["companyTel"])
                    print(item)
                    self.m.mongo_add(item)


    def test(self):
        url = 'http://www.80guakao.com/shengfen/sc/gonglugongcheng/23988.html'
        html = requests.get(url=url, headers=self.headers_forpage)
        print(html.text)
        res = etree.HTML(html.text)
        # print(res.xpath('//div[@class="pagination2"]//a[contains(text(),"下一页")]/@href'))
        # print(res.xpath('//div[@class="content"]//div//a/text()'))
        # print(html.text)
        # print(res.xpath('/html/body/div[7]/div[5]/div/div[6]/div[4]/div[3]/ul/div/span/a/@href'))
        # print(res.xpath('//div[@class="zhaopiner"]//li//span[contains(text(),"公司名称")]/parent::li/text()')[0]) #公司名称
        # print(res.xpath('//div[@class="zhaopiner"]//li//span[contains(text(),"专业要求")]/parent::li/text()')) #专业要求
        # print(res.xpath('//ul[@class="contacter"]//li//font/text()')[0]) #联系人
        phone_url_re=res.xpath('//ul[@class="contacter"]//li[@class="qqbm"]/a/@onclick')[0] #电话号码

        print(phone_url_re)
        par = re.compile("'.*?'")
        phone_url = re.findall(par, phone_url_re)[1].replace("'","") #电话号码url
        html = requests.get(url=phone_url, headers=self.headers_forpage)
        res = etree.HTML(html.text)
        phone = res.xpath('//div[@class="number"]//span[@class="num"]/text()')[0]
        print(phone)
        #Request URL: http://www.80guakao.com/box.php?part=seecontact_tel&id=54336&tel_base64=MTk5NTA0NTk5Mjc=
        # print(res.xpath('/html/body/div[7]/div[5]/div/div[6]/div[4]/div[3]/ul/div/span[1]/a/@href'))

    def run(self):
        self.get_category()
        self.get_sec_category()
        self.get_all_page()
        self.get_item_url()
        self.get_info()


if __name__ == '__main__':
    s = Gkspider()
    s.run()
    # s.test()


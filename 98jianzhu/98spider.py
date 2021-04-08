import os

import requests
from TOOLS.md5encode import md5encryption
from TOOLS.mongosave import MongoDB
from TOOLS.redissave import Redisclient
from lxml import etree
from PIL import Image
import pytesseract
from Func.fetchJX import FETCH
from Func.client import MongoDB
import base64
import sys
from time import sleep

class Spider98_zhaoping:
    def __init__(self):
        self.start_url = 'http://www.98pz.com/t59c11s1/1.html'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.r0 = Redisclient(0)
        self.r1 = Redisclient(1)
        self.f = FETCH()
        self.m = MongoDB('mongodb://localhost', 'cuiworkdb', "98guakao_hz_qz")

    def parse_next_page(self):
        self.r0.save_page_url(category_name='杭州求职', page_url=self.start_url)
        html = requests.get(url=self.start_url, headers=self.headers)
        sleep(0.5)
        while True:
            res = etree.HTML(html.text)
            try:
                next_page_url = res.xpath('//div[@class="pager"]//a[@class="next"]/@href')[0]
            except:
                break
            next_page_url = 'http://www.98pz.com/' + next_page_url
            print(next_page_url)
            self.r0.save_page_url(category_name='杭州求职', page_url=next_page_url)
            html = requests.get(url=next_page_url, headers=self.headers)

    def parse_item_url(self):
        while True:
            url = self.r0.get_page_url(category_name='杭州求职')
            try:
                html = requests.get(url=url, headers=self.headers)
                sleep(0.5)
            except:
                break
            res = etree.HTML(html.text)
            item_url_list = res.xpath('//td[@class="t"]//a[1]')[:-1]
            for one in item_url_list:
                url = one.xpath('./@href')[0]
                self.r1.save_item_url(category_name='杭州求职', url=url)

    def parse_data(self):
        while True:
            item = {}
            url = self.r1.get_item_url(category_name='杭州求职')
            if b'www' not in url:
                url = 'http://www.98pz.com' + str(url)
            try:
                html = requests.get(url=url, headers=self.headers)
                sleep(0.5)
            except Exception as e:
                print(e)
                continue
            res = etree.HTML(html.text)
            try:
                company_name = res.xpath('//span[@class="firm-name"]/a/@title')[0]
            except:
                continue
            # try:
            #     info = res.xpath('//li/i[contains(text(),"注册情况：")]/following-sibling::*/text()')[0]
            #     print(info)
            # except:
            #     continue

            contact_people = res.xpath('//li/i[contains(text(),"联 系 人：")]/following-sibling::*/text()')[0]
            print(contact_people)
            try:
                phone_url = res.xpath('//li/i[contains(text(),"固定电话：")]/following-sibling::*//img/@src')[0]
            except:
                try:
                    phone_url = res.xpath('//li/i[contains(text(),"手机号码：")]/following-sibling::*//img/@src')[0]
                except:
                    continue

            resourceMark = res.xpath('//li/i[contains(text(),"职位类型：")]/following-sibling::a//text()')
            resourceMark = resourceMark[0] + resourceMark[1]
            if phone_url == '':
                phone = ''
            else:
                try:
                    phone = self.rec_img(phone_url)
                except:
                    continue

            item['companyCity'] = '杭州'
            item['companyProvince'] = '浙江省'
            item['code'] = 'BUS_YT_ZZ'
            item['name'] = '资质'
            item['busCode'] = ''
            item['webUrl'] = '无'
            item['orgId'] = ''
            item['deptId'] = ''
            item['centreId'] = ''
            item["companyName"] = company_name
            item["outName"] = contact_people
            item["resourceRemark"] = resourceMark
            item["companyTel"] = phone
            item["ibossNum"] = None
            item['isDir'] = 0
            item['isShare'] = 0
            item["_id"] = md5encryption(item["companyTel"])
            print(item)
            self.m.mongo_add(item)

    def rec_img(self, img_url):

        url_b = img_url.split('data:image/gif;base64,')[1]
        url_b = url_b.encode()
        content = base64.b64decode(url_b)
        with open(r'G:\rec_pic\target.jpg', 'wb') as f:
            f.write(content)

        text = pytesseract.image_to_string(Image.open(r'G:\rec_pic\target.jpg').convert('RGB'))

        os.remove(r'G:\rec_pic\target.jpg')
        return text

    def test(self):
        self.parse_item_url()

    def run(self):
        self.parse_next_page()
        self.parse_item_url()

        self.parse_data()


# def restart_program():
#     python = sys.executable
#     os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    spider = Spider98_zhaoping()
    spider.run()
    # spider.test()

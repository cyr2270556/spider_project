import scrapy
from ..items import Scrapy78Item
import re
from TOOLS.md5encode import is_phone
import requests
from PIL import Image as image_P
import pytesseract
import os

class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['www.78gk.net']
    # eijing
    start_urls = ['https://www.78gk.net/11/']

    def parse(self, response):

        category_url_list = response.xpath('//div[@id="ni-flist"]//div//div//li//a')
        for i in category_url_list:
            url = i.xpath('./@href').get()
            # yield scrapy.Request(url=url, callback=self.parse_next_page_url
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_next_page_url)

    def parse_next_page_url(self, response):
        item_url_list = response.xpath('//div[@class="list_loop"]//ul//li[@class="lie2 alt1"]/a')
        for one in item_url_list:
            one_url = one.xpath('./@href').get()

            yield scrapy.Request(url=one_url, callback=self.parse_data)
        try:
            next_page_url = response.xpath('//div[@class="pagination2"]//a[contains(text(),"下一页")]/@href').get()
            if next_page_url:
                yield scrapy.Request(url=next_page_url, callback=self.parse_next_page_url)
                print(next_page_url)
        except Exception as e:
            print(e)


    def parse_data(self, response):
        companyName = response.xpath('//div[@class="username"]/a/text()').get()
        outName = response.xpath(
            '//ul[@class="contacter"]//li//span[contains(text(),"联系人")]/following-sibling::*/text() ').get()
        companyTel_url = response.xpath(
            '//ul[@class="contacter"]//li//span[contains(text(),"电话")]/following-sibling::a/@onclick').get()
        QQ_url = response.xpath('//ul[@class="contacter"]//li//span[contains(text(),"Q Q：")]/following-sibling::font/img/@src').get()
        self.download_img(QQ_url)
        resourceRemark = self.rec_pic()
        url = self.parse_phone(companyTel_url)

        item = Scrapy78Item()
        item["resourceRemark"] = 'qq:'+str(resourceRemark)
        item["companyName"] = companyName
        item["outName"] = outName
        yield scrapy.Request(url=url, meta={"meta_1": item}, callback=self.create_data)

    def create_data(self, response):
        companyTel = response.xpath('//span[@class="num"]/text()').get()
        if is_phone(companyTel):
            meta_1 = response.meta["meta_1"]
            companyName = meta_1["companyName"]
            if "企业管理" not in str(companyName):
                outName = meta_1["outName"]
                item = Scrapy78Item()
                item["companyName"] = companyName
                item["outName"] = outName
                item["companyTel"] = companyTel
                item["resourceRemark"]=meta_1["resourceRemark"]
                yield item

    def parse_phone(self, companyTel_url):
        par = re.compile("https:.*?\)")
        res = re.findall(par, companyTel_url)[0].split("')")[0]
        return res

    def rec_pic(self):
        """

        :param target_root:目标图像识别文件路径
        :return: 图像识别内容
        """
        try:
            text = pytesseract.image_to_string((image_P.open(r'G:\78挂靠\target.jpg')))
            os.remove(r'G:\78挂靠\target.jpg')
            return text
        except:
            return '无QQ号码'



    def download_img(self,img_url):
        #   res=s.fetch(url=url, headers=pic_headers, data=pic_data,method="post")
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'
        }
        try:
            res = requests.get(url=img_url,headers=headers)
            if res.status_code == 200:
                with open(r'G:\78挂靠\target.jpg', 'wb') as f:
                    f.write(res.content)
                return 1
            else:
                return 0
        except:
            print('没有qq号码')




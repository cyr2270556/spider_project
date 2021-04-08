# -*- coding: utf-8 -*-
import scrapy
from Guakao788.Guakao78.items import Guakao78Item
import sys, os
import re
sys.path.append(os.path.dirname(__file__) + os.sep + '../')


class Guakao78Spider(scrapy.Spider):
    name = 'guakao78'
    allowed_domains = ['www.78gk.net']
    start_urls = ['https://www.78gk.net/2/']


    def parse(self, response):
        category_url_list = response.xpath('//div[@class="ni-glist-section short"]//li//a')
        for i in category_url_list:
            url = i.xpath('./@href').get()
            print(url)
            item = Guakao78Item()
            item['url'] = url
            # yield scrapy.Request(url=url, callback=self.parse_next_page_url)
            yield item
    # def parse_next_page_url(self, response):
    #     try:
    #         url = response.xpath('//div[@class="pagination2"]//a[contains(text(),"下一页")]/@href').get()
    #         print(url)
    #         yield scrapy.Request(url=url, callback=self.parse_item_url)
    #         yield scrapy.Request(url=url, callback=self.parse_next_page_url)
    #     except Exception as e:
    #         print(e)
    #         print('此种类全部页数爬取完毕')
    #
    # def parse_item_url(self, response):
    #     # /html/body/div[7]/div[1]/table/tbody/tr/td[2]/a
    #     item_list = response.xpath('/html/body/div[3]/div[1]/div[8]/div[2]/ul/li[2]/a')
    #     for i in item_list:
    #         item_url = i.xpath('./@href').get()
    #         yield scrapy.Request(url=item_url, callback=self.parse)
    #
    # def parse(self, response):
    #     item = Guakao78Item()
    #     item["companyName"] = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[2]/div[1]/div/ul[1]/div[2]/a/text()').get()
    #     item["resourceRemark"] = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[1]/div[3]/div/ul/div[1]/li[4]/um/text()').get()
    #     item["outName"] = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[1]/div[3]/div/ul/ul/li[2]/font/text()').get()
    #     companyTel_url = response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[1]/div[3]/div/ul/ul/li[3]/a/@onclick').get()
    #     url=self.get_phone(companyTel_url)
    #     yield scrapy.Request(url=url,callback=self.parse_phone,meta={"meta_2":item})
    #
    #
    # def parse_phone(self,response):
    #     data = response.meta["meta_2"]
    #     item=Guakao78Item()
    #     item["companyTel"]=response.xpath('/html/body/div[1]/div[1]/span[1]/text()').get()
    #     item["companyName"]=data["companyName"]
    #     item["resourceRemark"]=data["resourceRemark"]
    #     item["outName"]=data["outName"]
    #
    #     yield item
    #
    # def get_phone(self,companyTel_url):
    #     #setbg('查看完整电话',420,520,'https://www.78gk.net/box.php?part=seecontact_tel&id=385977&tel_base64=MTgyMjQwNzA2MTY=')
    #     par=re.compile("'http:.*?'")
    #     companyTel=re.findall(par,companyTel_url)
    #     return companyTel
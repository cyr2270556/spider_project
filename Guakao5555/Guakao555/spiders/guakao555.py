# -*- coding: utf-8 -*-
import scrapy
from Guakao5555.Guakao555.items import Guakao555Item
import sys, os

sys.path.append(os.path.dirname(__file__) + os.sep + '../')


class Guakao555Spider(scrapy.Spider):
    name = 'guakao555'
    allowed_domains = ['http://www.555gk.com']

    def start_requests(self):
        url = 'http://www.555gk.com/zhaopin/r_0t_0c_0.html'
        yield scrapy.Request(url=url, callback=self.parse_region_url)

    def parse_region_url(self, response):
        item = Guakao555Item()
        region_url_list = response.xpath('/html/body/div[5]/div[2]/div[2]/a')[1:]

        for i in region_url_list:
            item["companyProvince"] = i.xpath('./text()').get()
            url = i.xpath('./@href').get()
            url = 'http://www.555gk.com' + url
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_next_page_url, meta={'meta_1': item})

    def parse_next_page_url(self, response):
        meta_1 = response.meta['meta_1']
        print(response.text)
        print(1)
        try:
            url = response.xpath('//*[@id="layui-laypage-0"]/a[7]/@href').get()
            url = 'http://www.555gk.com'+url
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_item_url, meta={'meta_1': meta_1})
            yield scrapy.Request(url=url, callback=self.parse_next_page_url, meta={'meta_1': meta_1})
        except Exception as e:
            print(e)
            print('此种类全部页数爬取完毕')

    def parse_item_url(self, response):
        # /html/body/div[7]/div[1]/table/tbody/tr/td[2]/a
        meta_1 = response.meta['meta_1']
        item_list = response.xpath('/html/body/div[7]/div[1]/table/tbody/tr/td[2]/a')
        for i in item_list:
            item_url = i.xpath('./@href').get()
            yield scrapy.Request(url=item_url, callback=self.parse, meta={'meta_1': meta_1})

    def parse(self, response):
        meta_1 = response.meta['meta_1']
        item = Guakao555Item()
        item["companyProvince"] = meta_1["companyProvince"]
        item["companyName"] = response.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/p').get()
        item["resourceRemark"] = response.xpath('/html/body/div[4]/div[1]/div[2]/ul[1]/li[1]/a[1]').get()
        item["outName"] = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]').get()
        item["companyTel"] = response.xpath('/html/body/div[4]/div[1]/div[3]/ul/li[2]/p').get()

        yield item

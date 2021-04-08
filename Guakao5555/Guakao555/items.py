# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Guakao555Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #地区
    companyProvince =scrapy.Field()
    #公司名
    companyName=scrapy.Field()
    #职称类型
    resourceRemark = scrapy.Field()
    #联系人
    outName = scrapy.Field()
    #电话号码
    companyTel = scrapy.Field()



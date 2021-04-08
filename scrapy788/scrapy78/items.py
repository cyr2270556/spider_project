# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy78Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    outName = scrapy.Field()

    companyName = scrapy.Field()

    companyTel = scrapy.Field()

    resourceRemark = scrapy.Field()
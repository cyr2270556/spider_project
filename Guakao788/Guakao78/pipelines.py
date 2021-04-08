# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Func.client import MongoDB
from TOOLS.md5encode import md5encryption

class Guakao78Pipeline(object):
    def open_spider(self,spider):
        #爬虫开始时候执行
        # # spider.hello = "world"  # 为spider对象动态添加属性，可以在spider模块中获取该属性值
        # # 可以开启数据库等
        # self.Mongo=MongoDB('mongodb://localhost', 'cuiworkdb', "78guakao_beijing")
        pass
    def process_item(self, item, spider):
        # item['companyProvince'] = "北京市"
        # item['companyCity']= '北京'
        # item['code'] = 'BUS_YT_ZZ'
        # item['name'] = '资质'
        # item['busCode'] = ''
        # item['webUrl'] ='无'
        # item['orgId'] =''
        # item['deptId'] = ''
        # item['centreId'] =  ''
        # item["ibossNum"] = None
        # item['isDir']= 0
        # item['isShare'] = 0
        # item["_id"] = md5encryption(item["companyTel"])
        # self.Mongo.mongo_add(item)
        return item

    def close_spider(self,spider):
        #爬虫结束时执行
        #可以关闭数据库
        pass

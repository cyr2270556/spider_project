# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from Func.client import MongoDB
from TOOLS.md5encode import md5encryption


class Scrapy78Pipeline:
    def open_spider(self, spider):
        # 爬虫开始时候执行
        # spider.hello = "world"  # 为spider对象动态添加属性，可以在spider模块中获取该属性值
        # 可以开启数据库等
        self.Mongo = MongoDB('mongodb://localhost', 'cuiworkdb', "78guakao_changsha")

    def process_item(self, item, spider):
        i = {}
        i['companyCity'] = "长沙"
        i['companyProvince'] = "湖南省"
        i['code'] = 'BUS_YT_ZZ'
        i['name'] = '资质'
        i['busCode'] = ''
        i['webUrl'] = '无'
        i['orgId'] = ''
        i['deptId'] = ''
        i['centreId'] = ''
        i["companyName"] = item["companyName"]
        i["outName"] = item["outName"]
        i["resourceRemark"] = item['resourceRemark']
        i["companyTel"] = str(item["companyTel"])
        i["ibossNum"] = None
        i['isDir'] = 0
        i['isShare'] = 0
        i['flag'] = 0
        i["_id"] = md5encryption(item["companyTel"])
        self.Mongo.mongo_add(i)
        print(i)
        return item





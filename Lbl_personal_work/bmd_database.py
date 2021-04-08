import pymongo
from TOOLS.mongosave import MongoDB

client = pymongo.MongoClient(host='localhost', port=27017)['cuiworkdb']['BMD20201224']

db1 = pymongo.MongoClient("mongodb://10.2.1.121:17017,10.2.1.122:17017,10.2.1.123:17017")["cuiworkdb"]["BMD20201224-1"]

a = []

for i in client.find():
    i['name'] = "知产"
    i['code'] = "BUS_YT_ZSCQ"
    a.append(i)


num=1
for i in a:
    if num<=40000:
        db1.insert_one(i)
        num+=1
    else:
        break
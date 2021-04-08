import pymongo

client = pymongo.MongoClient("mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017, 10.2.1.217:57017, 10.2.1.218:57017")
cli = client['shangbiao_db']['GongGao1657']

col = client['gateways_news']['Shangbiaoju']

c = cli.find()

n = 0
for i in c:
   try:
      col.insert(i)
      n += 1
   except Exception as e:
      print(e)
   print(n)
print('合计：{}'.format(n))
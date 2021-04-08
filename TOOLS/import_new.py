#从增量库里面导出flag=0的数据到clues表进行接口导入
from Func.client import MongoDB
# 导入接口（等号后接表名，数据库为）  https://dqk.dgg188.cn/api/import/import_data?ip=10.2.1.122:17017&docName=
import requests

m = MongoDB('mongodb://localhost', 'cuiworkdb', 'jianzhutong_hubei')
m2= MongoDB('10.2.1.121:17017', 'clues_resources', "BMD20210129-zhijiazhuang")
all_data=m.find_many("flag",0)
for one in all_data:
    m2.mongo_add(one)
m2.del_field()

#导入接口
# dbname='jianzhutong_guangzhou'
# data={"ip": "10.2.1.122:17017","docName":dbname}
# headers={
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
# "Accept-Encoding": "gzip, deflate, br",
# "Accept-Language": "zh-CN,zh;q=0.9",
# "Cache-Control": "no-cache",
# "Connection": "keep-alive",
# "Cookie": "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22172cc1339f4917-0029d8b329026-4353761-2073600-172cc1339f5818%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22172cc1339f4917-0029d8b329026-4353761-2073600-172cc1339f5818%22%7D",
# "Host": "dqk.dgg188.cn",
# "Pragma": "no-cache",
# "Sec-Fetch-Dest": "document",
# "Sec-Fetch-Mode": "navigate",
# "Sec-Fetch-Site": "none",
# "Sec-Fetch-User":"?1",
# "Upgrade-Insecure-Requests":"1",
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
# }
# res=requests.post(url='https://dqk.dgg188.cn/api/import/import_data?ip=10.2.1.122:17017&docName=',data=data,headers=headers)
# print('导入%s条'%(res.text))

from collections import Counter
from Func.client import MongoDB
# print(Counter([1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4]))
# Counter({2: 4, 4: 4, 3: 3, 1: 1})
from threadfunc import start_thread
from threading import Thread

# m3 = MongoDB('10.2.1.121:17017', 'clues_resources', "test")
# a=[{"companyName": "123","a":1,"companyTel":"13258399376"},{"companyName":"123","a":2,"companyTel":"123"},{"companyName":"123","a":3,"companyTel":"123"},{"companyName":"456","a":4,"companyTel":"0"}]
# for i in a:
#     m3.mongo_add(i)

# list_company_name=[]
# list_data=m3.find_all()
# for i in list_data:
#     list_company_name.append(i["companyName"])
#
# myset = set(list_company_name)
# for i in myset:
#     if list_company_name.count(i) > 1:
#         tem = m3.mongo_find_company(i).next()
#         m3.find_one_and_remove(i)
#         m3.mongo_add(tem)
#         # m2.mongo_add(k for k in list_data if list_data["companyName"]==i)
#     else:
#         continue

def print_test():
    for i in range(1000):
        print(i)

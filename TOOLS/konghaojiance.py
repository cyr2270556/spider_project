#空号检测文件
from Func.client import MongoDB

db = MongoDB('10.2.1.121:17017', 'clues_resources', "BMD_sort")
db2 = MongoDB('mongodb://localhost', 'cuiworkdb', 'BMD20210201-chengdu-check')

all_data = db.find_all()
# all_data=db.find_many("flag",0)
#mongo 电话数据导出为txt，拿去空号检测
with open('BMD_sort', 'w') as f:
    for i in all_data:
        phone = i["companyTel"]
        f.write(str(phone) + '\n')

#将活跃号数据导入xxxx-check表
# huoyue_list = []
# with open('活跃号(实号).txt','r',encoding='utf-8') as f:
#     for line in f:
#         huoyue_list.append(line.strip())
#
# for i in all_data:
#     if i["companyTel"] in huoyue_list:
#         db2.mongo_add(i)
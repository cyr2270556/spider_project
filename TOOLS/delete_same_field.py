#去重策略文件
from Func.client import MongoDB
from md5encode import is_phone
m1 = MongoDB('mongodb://localhost', 'cuiworkdb', "9guakao_zhengzhou")
m2 = MongoDB('10.2.1.121:17017', 'clues_resources', "BMD_sort")
m3 = MongoDB('10.2.1.121:17017', 'clues_resources', "test")
m4 = MongoDB('10.2.1.121:17017', 'clues_resources', "BMD_20210205_push")
m5 = MongoDB('10.2.1.121:17017', 'clues_resources', "test")

# m5 = MongoDB('10.2.1.121:17017', 'clues_resources', "jianzhutong_shengzheng")
# m5 = MongoDB('10.2.1.121:17017', 'clues_resources', "BMD20201224-4")
# 导入clues,只有这个才能推送数据
# m1.mong_find_many_updata({"companyCity": "成都"}, {"isDir": 0})


#去重策略1  将小表全部聚集到BMD_sort大表中做_id去重
# all_data = m1.find_all()
# for i in all_data:
#     m2.mongo_add(i)

# 去重策略2  同名公司名去重策略
#第一版弃用
# list_data = list(m2.find_all())
# for i in range(len(list_data)):
#    for k in range(i+1, len(list_data)):
#        if list_data[i]["companyName"] == list_data[k]["companyName"]:
#            list_data[k]["companyName"] = "None"


# list_company_name = []
# list_data = m2.find_all()
# for i in list_data:
#     list_company_name.append(i["companyName"])
#
# myset = set(list_company_name)
# for i in myset:
#     if list_company_name.count(i) > 1:
#         tem = m2.mongo_find_company(i).next()
#         m2.find_one_and_remove(i)
#         m2.mongo_add(tem)
#         # m2.mongo_add(k for k in list_data if list_data["companyName"]==i)
#     else:
#         continue

#去重策略3 去重非手机号电话号码
# all_data=m2.find_many("flag",0)
all_data = m2.find_all()
for i in all_data:
    if is_phone(i["companyTel"]):
       continue
    else:
        m2.remove_nophone(i["companyTel"])
        print("删除非手机号数据",i["companyTel"])

#去重策略4 导出电话号码txt文件，上传刀鱼，下载检测成功文件，进行对比插入


# all_data=m2.find_many("flag",0)
# # with open('BMD_sort.txt', 'w') as f:
# #     for i in all_data:
# #         phone = i["companyTel"]
# #         f.write(str(phone) + '\n')
#
# huoyue_list = []
# with open('活跃号(实号).txt','r',encoding='utf-8') as f:
#     for line in f:
#         huoyue_list.append(line.strip())
#
# for i in all_data:
#     if i["companyTel"] not in huoyue_list:
#         print("删除空号",i["companyTel"])
#         m2.remove_nophone(i["companyTel"])

#导入接口策略(数据量小时使用),导出为push表
# all_data=m2.find_many("flag",0)
# for i in all_data:
#     m4.mongo_add(i)

#接口url  https://dqk.dgg188.cn/api/import/import_data?ip=10.2.1.122:17017&docName=

#sort表最终处理，将推送的数据flag改为1

# m2.change_flag()


#导入接口策略(数据量过大使用)
# count = 0
# gd_data = m1.find_all()
# for i in gd_data:
#     # if count <= 3000:
#         m2.mongo_add(i)
    # elif count <= 6000:
    #     m3.mongo_add(i)
    # elif count<=9000:
    #     m4.mongo_add(i)
    # else:
    #     m5.mongo_add(i)
    # count += 1
#all_data = m3.find_all()








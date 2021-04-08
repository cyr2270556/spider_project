from Func.client import MongoDB

m1 = MongoDB('mongodb://localhost', 'cuiworkdb', "jianzhutong_shanghai")
m2 = MongoDB('10.2.1.121:17017', 'clues_resources', "jianzhutong_shanghai")
# m3 = MongoDB('10.2.1.121:17017', 'clues_resources', "jianzhutong_guangzhou")
# m4 = MongoDB('10.2.1.121:17017', 'clues_resources', "jianzhutong_foshan")
# m5 = MongoDB('10.2.1.121:17017', 'clues_resources', "jianzhutong_shengzheng")

# m5 = MongoDB('10.2.1.121:17017', 'clues_resources', "BMD20201224-4")
# 导入clues,只有这个才能推送数据

# m1.mong_find_many_updata({"companyCity": "成都"}, {"isDir": 0})


# all_data = m1.find_all()
# for i in all_data:
#     print(i)

count = 0
gd_data = m1.find_all()
for i in gd_data:
    # if count <= 3000:
        m2.mongo_add(i)
    # elif count <= 6000:
    #     m3.mongo_add(i)
    # elif count<=9000:
    #     m4.mongo_add(i)
    # else:
    #     m5.mongo_add(i)
    # count += 1
#all_data = m3.find_all()


# 相同公司名去重
# list_data = list(m1.find_all())
# for i in range(len(list_data)):
#    for k in range(i+1, len(list_data)):
#        if list_data[i]["companyName"] == list_data[k]["companyName"]:
#            list_data[k]["companyName"] = "None"
#
#for i in list_data:
   # print(i)
    #m4.mongo_add(i)
#
#m4.find_one_remove_same()

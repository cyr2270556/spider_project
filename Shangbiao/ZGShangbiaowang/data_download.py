# 数据爬取模块
# 爬取数据放入mongo

from selenium import webdriver
from time import sleep
from TOOLS.mongosave import MongoDB

import requests
from time import sleep
import json



pic_url = "http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/imageView.html?O56fzBVE=5eplSW8Ue6wDcXH09g_OkciKAveKxT3sc3dolHVUt6KwHI9EUsUDLtN0qvlYGBIHeASXxkgTPARhCJ1FalN9bDbbw9xETXPCa6XgZ6fVy825H0GAtSYEMi0EPASZJiN5X9xmuSQ6KgG5g57bYV3HKrTCfp56SWZm80Rq9H0yRz9Kd4KFMCsZv2iJ2TcT3MwnXknL8PTRAsMg9KitIv7hO1HSBuIVZAPPnT4VzjA3dCMLZXFNxwchKXpQlsRuEGBm4UFLpSA9z_SDokZunFUv1pker4yNxfpdG5qVAMJTQTfdQeDIGSR3foM91g8zm7PkRfvon_VFbwXDGHPYsrjaoYXrZLquIy.pQypTDWkAKIRpRZee65Vin4s9CfuBO1OTG"

pic_headers = {
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip,deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length":"54",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"goN9uW4i0iKzS=5k.OoVYCbjTAf3bwRIXZ3dkPLdG0x33opO9zk1H4aeBZSKp82yGGbeib_50wWarq5OuyL37G9oJs_UxMn7omDoa;__jsluid_h=d7d74f1ae76f0f9af7a8abd3085325de; 018f9ebcc3834ce269=cec633fff26cf2c5b69e553a367db190; tmas_cookie=2272.7688.15400.0000; JSESSIONID=0000s0T8gRL9PAwpGEP_2SlddMb:1bm112lvs; goN9uW4i0iKzT=5UdFBCTdC.5LqqqmCCy5F1GO5gEbusUM5YNIL89_gaoFSc.VB_Pa52PLMfKmbKLoPNsPrAAandUi87P8BI2Ac_90IGsebwf6.bxRyWSqLRnGgV6DCLZGMh_bit7_hmsSDnJ0dIM3hsOuipSb1Fe5MGCV7ckvFTpJmNfqcTW1ugtkMpEQs6P2rNquCvbOH4Un5AWtWyVqL.mpeSP5bTMPQctYMCEiptvl8qAJd0BrOwL4I35UZuRHTeCRNmoFYKIre69VH0jgTpDz8T2H6UEDnqGNJQk5NU8lwCaRoqCG8xaoYfkZRKiUnMuT1UxBj3cAOyJha5a0sWmDZh1fsQdMo6Z",
    "Host":"wsgg.sbj.cnipa.gov.cn:9080",
    "Origin":"http://wsgg.sbj.cnipa.gov.cn:9080",
    "Referer":"http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
}

pic_json_que = {
    "O56fzBVE":"5eplSW8Ue6wDcXH09g_OkciKAveKxT3sc3dolHVUt6KwHI9EUsUDLtN0qvlYGBIHeASXxkgTPARhCJ1FalN9bDbbw9xETXPCa6XgZ6fVy825H0GAtSYEMi0EPASZJiN5X9xmuSQ6KgG5g57bYV3HKrTCfp56SWZm80Rq9H0yRz9Kd4KFMCsZv2iJ2TcT3MwnXknL8PTRAsMg9KitIv7hO1HSBuIVZAPPnT4VzjA3dCMLZXFNxwchKXpQlsRuEGBm4UFLpSA9z_SDokZunFUv1pker4yNxfpdG5qVAMJTQTfdQeDIGSR3foM91g8zm7PkRfvon_VFbwXDGHPYsrjaoYXrZLquIy.pQypTDWkAKIRpRZee65Vin4s9CfuBO1OTG"
}

pic_data = {
    "id": "e48b92f76f4c83dc016f5beebb021f08",
    "pageNum": "",
    "flag": "1",
}



#302 开始 看f12
def pic_download(num):

    pic_data["pageNum"] = str(num)
    res = requests.post(url=pic_url, headers=pic_headers, data=pic_data, json=pic_json_que)
    res_json = json.loads(res.text)
    print(res_json)
    pic_url_list = res_json["imaglist"]
    if num == 302:
        pic_url_list = pic_url_list[3:]
    return pic_url_list


category_dict={"送达公告":"TMSDGG"}


###固定代码
def data_spdier(collection_name, periods, category,total_page,pic_url_list):
    """

    :param collection_name:存入mongo的集合名 str
    :param periods: 公告期数 str
    :param category: 公告种类（例如送达公告，无效公告等）str
    :param total_page: 公告数据总页数 int
    :return: 本地cuiworkdb collection_name 中查看数据
    """

    db = MongoDB('mongodb://localhost', 'cuiworkdb', collection_name)

    driver = webdriver.Chrome()

    driver.implicitly_wait(10)

    driver.get('http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=')

    driver.find_element_by_xpath('//input[@id="annNum"]').send_keys(periods)
    # 点击公告类型
    sleep(0.2)
    driver.find_element_by_xpath('//select[@id="annTypes"]').click()
    # 点击送达公告
    #'//select[@id="annTypes"]//option[@value="TMSDGG"]'
    driver.find_element_by_xpath('//select[@id="annTypes"]//option[@value="{}"]'.format(category)).click()
    # 点击查询
    driver.find_element_by_xpath('//input[@name="annSearchBut"]').click()

    sleep(2)
    ###

    ####此处代码爬取数据
    ###每个都是20个数据，查看需要处理
    # 注册号  //table//tr[@class="evenBj"]/td[5]
    # 申请人 //table//tr[@class="evenBj"]/td[6]
    # 商标名称 //table//tr[@class="evenBj"]/td[7]
    # 查看 //table//tr[@class="evenBj"]/td[8]

    count = 0
    page = 1
    number=0
    while True:
        # 终止页数
        if page == total_page+1:
            break
        sleep(1)
        register_num = driver.find_elements_by_xpath('//table//tr[@class="evenBj"]/td[5]')
        company_name = driver.find_elements_by_xpath('//table//tr[@class="evenBj"]/td[6]')
        brand_name = driver.find_elements_by_xpath('//table//tr[@class="evenBj"]/td[7]')
        for i in range(len(register_num)):
            item = {}
            item['_id'] = count+1
            item['num'] = periods
            item['category'] = '送达公告'
            item['type'] = ''
            item['register_num'] = register_num[i].text
            try:
                item['company_name'] = company_name[i].text
            except:
                item['company_name'] = ''
            try:
                item['brand_name'] = brand_name[i].text
            except:
                item['brand_name'] = ''
            if i % 2 == 0 or i ==0 :
                item['pic_url'] = pic_url_list[number]
                print(count)
                #0 1 2 3 4 5 6 7
                #
            else:
                item['pic_url']=pic_url_list[number-1]
                number-=1
            print(item)
            db.mongo_add(item)
            number+=1
            count += 1
        sleep(2)
        driver.find_element_by_xpath('//div[@id="pages"]//td[8]//a//span[2]').click()
        page += 1
        sleep(1)
#r'"TMSDGG"'




###########################################################################






# for i in range(4, 2262, 20):
#     pic_data["pageNum"] = i
#     res = requests.post(url=pic_url, headers=pic_headers, data=pic_data, json=pic_json_que)
#     res_json = json.loads(res.text)
#     print(res_json["imaglist"])
#     sleep(5)

num = 302
pic_url_list=[]
while True:
    if num > 2259:
        break
    pic_url_list.extend(pic_download(num))
    num+=20
print(pic_url_list)

data_spdier('Shangbiao_GG-1678','1678',category_dict["送达公告"],227,pic_url_list)


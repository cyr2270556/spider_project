#备份文件



# 数据爬取模块
#爬取数据放入mongo

from selenium import webdriver
from time import sleep
from TOOLS.mongosave import MongoDB
from pykeyboard import *
from pymouse import *

###固定代码
k = PyKeyboard()
m = PyMouse()

db = MongoDB('mongodb://localhost', 'cuiworkdb', 'Shangbiao_GG')

driver = webdriver.Chrome()

driver.implicitly_wait(10)

driver.get('http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=')

num = '1637'
# 输入期数（可更改）


driver.find_element_by_xpath('//input[@id="annNum"]').send_keys(num)
# 点击公告类型
sleep(0.2)
driver.find_element_by_xpath('//select[@id="annTypes"]').click()
# 点击送达公告
driver.find_element_by_xpath('//select[@id="annTypes"]//option[@value="TMSDGG"]').click()
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
while True:
    # 终止页数
    if page == 221:
        break
    register_num = driver.find_elements_by_xpath('//table//tr[@class="evenBj"]/td[5]')
    company_name = driver.find_elements_by_xpath('//table//tr[@class="evenBj"]/td[6]')
    brand_name = driver.find_elements_by_xpath('//table//tr[@class="evenBj"]/td[7]')

    for i in range(len(register_num)):
        item = {}
        item['_id'] = count
        item['num'] = num
        item['category'] = '送达公告'
        item['type'] = ''
        item['register_num'] = register_num[i].text
        try:
            item['company_name'] = company_name[i].text
        except:
            item['company_name']=''
        try:
            item['brand_name'] = brand_name[i].text
        except:
            item['brand_name']=''
        print(item)
        db.mongo_add(item)
        count += 1
    sleep(2)
    driver.find_element_by_xpath('//div[@id="pages"]//td[8]//a//span[2]').click()
    page += 1
    sleep(1)

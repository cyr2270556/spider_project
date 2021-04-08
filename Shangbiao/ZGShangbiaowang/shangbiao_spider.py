#2021/1/11 弃用

# 图片下载模块
#图片下载到“下载”文件夹，按照数字顺序重命名

from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from TOOLS.mongosave import MongoDB
import os
from pykeyboard import *
from pymouse import *

###固定代码

k = PyKeyboard()
m = PyMouse()

db = MongoDB('mongodb://localhost', 'cuiworkdb', 'Shangbiao_GG')

driver = webdriver.Chrome()
driver.maximize_window()

driver.implicitly_wait(10)

driver.get('http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=')

num = '1677'
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
driver.find_element_by_class_name('look').click()
sleep(0.5)
count = 1
#跳转页面

#
driver.find_element_by_id('nowPage').click()
# driver.find_element_by_id('nowPage').click()
k.tap_key(k.backspace_key)
k.tap_key(k.backspace_key)
k.tap_key(k.delete_key)
k.tap_key(k.delete_key)
sleep(0.2)
driver.find_element_by_id('nowPage').send_keys("2420")
sleep(0.1)
k.tap_key(k.enter_key)
sleep(3.5)
#1385
#下载图片
for i in range(2420, 4249):


    # 鼠标右键
    # else:
    img = driver.find_element_by_id('imgs')

    ActionChains(driver).context_click(img).perform()
    sleep(0.2)
    k.tap_key('v')
    sleep(0.5)
    k.type_string("{}.jpg".format(i))
    sleep(1)
    k.tap_key(k.enter_key)

    sleep(1)
    if os.path.exists(r'C:\Users\admin\Downloads\{}.jpg'.format(i)):
        driver.find_element_by_id('nowPage').click()
        sleep(0.3)
        k.tap_key(k.backspace_key)
        k.tap_key(k.backspace_key)
        k.tap_key(k.backspace_key)

        k.tap_key(k.backspace_key)
        k.tap_key(k.delete_key)
        sleep(0.5)
        driver.find_element_by_id('nowPage').send_keys("{}".format(i+1))
        k.tap_key(k.enter_key)
    else:
        sleep(0.5)
        driver.find_element_by_link_text('下一页').click()
        sleep(1.8)
    sleep(1)

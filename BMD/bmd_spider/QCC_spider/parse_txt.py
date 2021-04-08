from lxml import etree
import os
# 未封装完成 for循环内规则不可复用

def parse(xpath_rule1, xpath_rule2, xpath_rule3):
    with open(r'C:\Users\admin\Documents\test.txt', 'r', encoding='utf-8') as f:
        html = f.read()
        res = etree.HTML(html)
        # company_name_list = res.xpath('//div[@class="row"]//table//tr//td[2]/a/text()')
        # company_boss_list = res.xpath('//div[@class="row"]//table//tr//td[2]/p/a/text()')
        # company_phone_list = res.xpath('//div[@class="row"]//table//tr//td[2]/p[2]/text()')

        company_name_list = res.xpath(xpath_rule1)
        company_boss_list = res.xpath(xpath_rule2)
        company_phone_list = res.xpath(xpath_rule3)

        # print(company_phone_list[1].strip())
        for i in range(len(company_name_list)):
            company_name = company_name_list[i]
            company_boss = company_boss_list[i]
            company_phone = company_phone_list[(i + 1) * 2 + i - 1].strip()
            print(company_name)
            print(company_boss)
            print(company_phone)
    if os.path.exists(r'C:\Users\admin\Documents\test.txt'):
        os.remove(r'C:\Users\admin\Documents\test.txt')
        print("文件已删除")
    else:
        print("文件不存在")


with open(r'C:\Users\admin\Desktop\test.txt', 'r', encoding='utf-8') as f:
    html = f.read()
    res = etree.HTML(html)
    company_name_list = res.xpath('//div[@class="row"]//table//tr//td[2]/a/text()')
    company_boss_list = res.xpath('//div[@class="row"]//table//tr//td[2]/p/a/text()')
    company_phone_list = res.xpath('//div[@class="row"]//table//tr//td[2]/p[2]/text()')

    # print(company_phone_list[1].strip())
    for i in range(len(company_name_list)):
        company_name = company_name_list[i]
        company_boss = company_boss_list[i]
        company_phone = company_phone_list[(i + 1) * 2 + i - 1].strip()

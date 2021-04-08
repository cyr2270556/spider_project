# 读取excel文件，存入本地mongo库
import re
import xlrd
from BMD.bmd_excel.public import city, Format_code
from TOOLS.md5encode import md5encryption
from BMD.bmd_excel.public import db


# from Func.client import MongoDB

# db1 = MongoDB('mongodb://10.2.1.121:17017,10.2.1.122:17017,10.2.1.123:17017', 'clues_resources', 'ZZ_20201214_rollback')


def read_exel(target_city, Format, shiyebu_ID, bumeng_ID, zhongxing_ID, one_address):
    """

    :param target_city: 目标城市名称
    :param Format: 业态名称
    :param shiyebu_ID: 事业部ID
    :param bumeng_ID: 部门ID
    :param zhongxing_ID: 中心ID
    :param document_address: excel文件地址
    :return: 字典类型数据
    """
    # book = xlrd.open_workbook(r'C:\Users\admin\Desktop\新建文件夹\查企业_高级搜索_企查查(46289011).xls')
    book = xlrd.open_workbook(one_address)
    sheet = book.sheets()[0]
    # 公司名称
    company_name = sheet.col_values(0)[2:]
    # 法定代表人 #
    Legal_representative = sheet.col_values(2)[2:]
    # 注册资本 #
    registered_capital = sheet.col_values(3)[2:]
    # 成立日期
    incorporation_date = sheet.col_values(3)[2:]
    # 经营状态
    business_status = sheet.col_values(4)[2:]
    # 所属省份 #
    province = sheet.col_values(6)[2:]
    # 所属市区 #
    area = sheet.col_values(7)[2:]
    # 公司类型 #
    # type = sheet1.col_values(18)[2:]
    # 统一社会信用代码 #
    # social_credit_code = sheet1.col_values(13)[2:]
    # 纳税人识别号 #
    # tax_code = sheet1.col_values(14)[2:]
    # 联系方式 #
    tel = sheet.col_values(9)[2:]
    # 其他联系方式
    other_tel = sheet.col_values(10)[2:]
    # 所属行业
    # Industry = sheet.col_values(19)[2:]
    # 企业地址
    # address = sheet.col_values(22)[2:]
    # 经营范围
    # business_scope = sheet.col_values(24)[2:]
    for i in range(len(company_name)):
        item = {}
        if company_name[i] == '':
            item['companyName'] = '无'
        else:
            item['companyName'] = company_name[i]
        try:
            if tel[i].startswith('1') and tel[i] is not '' and len(tel[i]) == 11:
                item['companyTel'] = tel[i]
                item['outName'] = Legal_representative[i]
                item['companyCity'] = target_city
                item['companyProvince'] = city[target_city]
                item['name'] = Format
                item['code'] = Format_code[Format]
                item['busCode'] = ''
                item['webUrl'] = '无'
                # item['resourceRemark'] = '定向资源' + '  公司名称:' + company_name[i] + ';法定代表人:' + Legal_representative[i] \
                #                          + ';注册资本:' + registered_capital[i] + ';成立日期:' + \
                #                          incorporation_date[i] + ';经营状态:' + business_status[i] + ';所属省份:' + province[i] \
                #                          + ';所属市区:' + area[i]
                # """+ ';公司类型:' + col3_values8[i] + ';统一社会信用代码:' \
                # + col3_values9[i] + ';纳税人识别号：' + col3_values10[i] + ';所属行业：' + col3_values14[i] \
                # + '; 企业地址：' + col3_values15[i] + ';经营范围：' + col3_values16[i]"""
                item['resourceRemark'] =''
                # 工号 类型 int
                item['ibossNum'] = None
                # 事业部ID 字符串
                # item['orgId'] = '7702432305591226368'
                item['orgId'] = shiyebu_ID
                # 部门ID 字符串
                # item['deptId'] = '7702433405966880768'
                item['deptId'] = bumeng_ID
                # 中心ID 字符串
                # item['centreId'] = '7702432778532556800'
                item['centreId'] = zhongxing_ID
                # 是否定向
                item['isDir'] = 0
                # 是否分润
                item['isShare'] = 0
                item['_id'] = md5encryption(item['companyTel'])
                print(item)
                db.mongo_add(item)

            else:
                phone = re.findall(r'\d{11}', other_tel[i])
                if len(phone) != 0:
                    item['companyTel'] = phone[0]
                    item['outName'] = Legal_representative[i]

                    item['companyCity'] = target_city
                    item['companyProvince'] = city[target_city]
                    item['name'] = Format
                    item['code'] = Format_code[Format]
                    item['busCode'] = ''
                    item['webUrl'] = '无'
                    # item['resourceRemark'] = '定向资源' + '  公司名称:' + company_name[i] + ';法定代表人:' + Legal_representative[i] \
                    #                          + ';注册资本:' + registered_capital[i] + ';成立日期:' + \
                    #                          incorporation_date[i] + ';经营状态:' + business_status[i] + ';所属省份:' + \
                    #                          province[i] \
                    #                          + ';所属市区:' + area[i]
                    item['resourceRemark'] =''
                    # 工号 类型 int
                    item['ibossNum'] = None
                    # 事业部ID 字符串
                    item['orgId'] = shiyebu_ID
                    # 部门ID 字符串
                    item['deptId'] = bumeng_ID
                    # 中心ID 字符串
                    item['centreId'] = zhongxing_ID
                    # 是否定向
                    item['isDir'] = 0
                    # 是否分润
                    item['isShare'] = 0
                    item['_id'] = md5encryption(item['companyTel'])
                    print(item)
                    db.mongo_add(item)

        except Exception as e:
            print(e)

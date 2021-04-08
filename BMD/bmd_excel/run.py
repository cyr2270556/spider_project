# 执行文件
from BMD.bmd_excel.excel_handle import read_exel
from BMD.bmd_excel.public import document_address, target_city, Format, shiyebu_ID, bumeng_ID, zhongxing_ID
from TOOLS.threadfunc import start_thread

"""
listdir传入未清洗文件二层文件绝对路径
read_exel传入目标城市名字，业态名字，事业部ID，部门ID，中心ID，excel文件路径
public.py文件决定mongo数据库用哪个
"""
import os


# def run_this(document_address, target_city, Format, shiyebu_ID, bumeng_ID, zhongxing_ID):
#     """
#
#     :param document_address: excel文件路径
#     :param target_city: 城市名字
#     :param Format: 业态名字
#     :param shiyebu_ID: 事业部ID
#     :param bumeng_ID: 部门ID
#     :param zhongxing_ID: 中心ID
#     :return:
#     """
#     document_list = os.listdir(document_address)
#     for one in document_list:
#         absolute_path = document_address + r'\%s' % one
#         read_exel(target_city, Format, shiyebu_ID,
#                   bumeng_ID, zhongxing_ID,
#                   eval(repr(absolute_path)))


def run_this(document_address, target_city, Format, shiyebu_ID, bumeng_ID, zhongxing_ID, ):
    """
    :param document_address: excel文件路径
    :param target_city: 城市名字
    :param Format: 业态名字
    :param shiyebu_ID: 事业部ID
    :param bumeng_ID: 部门ID
    :param zhongxing_ID: 中心ID
    :return:

    """
    document_list = os.listdir(document_address)

    for one in document_list:
        absolute_path = document_address + r'\%s' % one
        read_exel(target_city=target_city, Format=Format, shiyebu_ID=shiyebu_ID,
                  bumeng_ID=bumeng_ID, zhongxing_ID=zhongxing_ID,
                  one_address=eval(repr(absolute_path)))


# run_this(document_address, target_city, Format, shiyebu_ID, bumeng_ID, zhongxing_ID)

parameters = document_address, target_city, Format, shiyebu_ID, bumeng_ID, zhongxing_ID

if __name__ == '__main__':
    start_thread(run_this, 5, document_address, target_city, Format, shiyebu_ID, bumeng_ID, zhongxing_ID)

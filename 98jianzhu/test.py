import os
import sys

import requests
from PIL import Image
import pytesseract
from Func.fetchJX import FETCH
import base64
from lxml import etree



# a= 'http://www.98pz.com/info/64467767.html'
# html = requests.get(url='http://www.98pz.com/info/64467767.html')
#
# res= etree.HTML(html.text)
# print(res.xpath('//li/i[contains(text(),"固定电话：")]/following-sibling::*//img/@src')[0])




# def download_img( img_url):
#     f = FETCH()
#     # res = f.fetch(url=img_url, method="get")
#     res = requests.get(url=img_url)
#     if res.status_code == 200:
#         with open(r'G:\rec_pic\target.jpg', 'wb') as f:
#             f.write(res.content)
#         return 1
#     else:
#         return 0
#
#
# #
# url = 'data:image/gif;base64,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'
# url2 = b'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'

# def rec_img(img_url):
#     url_b=img_url.split('data:image/gif;base64,')[1]
#     url_b=url_b.encode()
#     content = base64.b64decode(url_b)
#     with open(r'G:\rec_pic\target.jpg', 'wb') as f:
#         f.write(content)
#     text = pytesseract.image_to_string((image_P.open(r'G:\rec_pic\target.jpg')))
#     # os.remove(r'G:\rec_pic\target.jpg')
#     return text

# def rec_pic():
#     text = pytesseract.image_to_string(Image.open(r'G:\rec_pic\target.jpg').convert('RGB'))
#     print(text)
#
# rec_pic()




# 导入 base64模块
# import base64
#
# # 给定需要转换的字符串
# str1 = "你好"
#
# # 需要转成2进制格式才可以转换，所以我们这里再手动转换一下
# result = base64.b64encode(str1.encode())
#
# # 打印转换后的结果
# print('转换后的结果 -->',result)
#
# # 再把加密后的结果解码
# temp = base64.b64decode(result)
#
# # 同样的，解码后的结0果是二进制，我们再转换一下
# print('解密后的结果 --> ',temp.decode())

# def restart_program():
#     print('ready')
#     python = sys.executable
#     os.execl(python, python, *sys.argv)
#
# for i in range(10):
#     print(i)
# restart_program()
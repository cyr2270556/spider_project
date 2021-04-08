from PIL import Image
import pytesseract
import requests
import os
import re
from time import sleep


def get_phone(picurl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    res = requests.get(picurl, headers=headers)
    file_name = 'C://Users//admin//Desktop//Big.jpg'
    a = os.path.exists(file_name)
    if a is False:
        with open(file_name, 'wb') as f:
            f.write(res.content)

    text = pytesseract.image_to_string(Image.open(file_name))
    cellphone = re.compile("\d+", re.S)
    phone = cellphone.findall(text)
    if not phone:
        telphone = re.compile("\d+.*?\d+", re.S)
        phone = telphone.findall(text)
    os.remove(file_name)
    return phone

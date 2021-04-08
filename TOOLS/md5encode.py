# md5加密

import hashlib
import re

def md5encryption(target):
    """

    :param target: md5加密目标
    :return: 返回加密数值
    :mark: 如果出现b串问题，先decode再encode
    """
    return hashlib.md5(target.encode(encoding='utf-8')).hexdigest()


def phone_encrypte(phone):
    # 将电话号码进行md5加密
    md5 = hashlib.md5()
    md5.update(phone.encode())
    md_phone = md5.hexdigest()
    return md_phone

def is_phone(phone):
    # phone_par = re.compile('^[1]([3-9])[0-9]{9}$')
    phone_par=re.compile('\d{11}')
    res = re.findall(phone_par, str(phone))
    if not res:
        return False
    else:
        return True


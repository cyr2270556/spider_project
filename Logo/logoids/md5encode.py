import hashlib

def id_encrypte(target):
    #将传入数据进行md5加密
    md5=hashlib.md5()
    #byte数据要用decode
    md5.update(target.decode().encode())
    data=md5.hexdigest()
    return data
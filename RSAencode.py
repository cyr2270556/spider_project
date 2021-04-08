import rsa

# 先生成一对密钥，然后保存.pem格式文件，当然也可以直接使用
(pubkey, privkey) = rsa.newkeys(1024)
pub = pubkey.save_pkcs1()
pubfile = open('public.pem', 'w+')
pubfile.write(pub.decode())
pubfile.close()
pri = privkey.save_pkcs1()
prifile = open('private.pem', 'w+')
prifile.write(pri.decode())
prifile.close()

# load公钥和密钥
message = 'hello' #加密字符串
with open('public.pem') as publickfile:
    p = publickfile.read()
pubkey = rsa.PublicKey.load_pkcs1(p.encode())
with open('private.pem') as privatefile:
    p = privatefile.read()
privkey = rsa.PrivateKey.load_pkcs1(p.encode())

# 用公钥加密、再用私钥解密
crypto = rsa.encrypt(message.encode(), pubkey)
message = rsa.decrypt(crypto, privkey)
print(message)

# sign 用私钥签名认真、再用公钥验证签名
signature = rsa.sign(message, privkey, 'SHA-1')
rsa.verify(b'hello', signature, pubkey )
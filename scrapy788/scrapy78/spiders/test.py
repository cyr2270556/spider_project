# import requests
# from lxml import etree
# url='https://www.78gk.net/440/'
# headers={
#
# "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
# "accept-encoding":"gzip,deflate,br",
# "accept-language":"zh-CN,zh;q=0.9",
# "cache-control":"no-cache",
# "cookie":"Hm_lvt_e0355b37aacebb0e9b79c5ba05d6678f=1612319315; jweu__cityid=2; Hm_lpvt_e0355b37aacebb0e9b79c5ba05d6678f=1612410123",
# "pragma":"no-cache",
# "sec-fetch-mode":"navigate",
# "sec-fetch-site":"none",
# "sec-fetch-user":"?1",
# "upgrade-insecure-requests":"1",
# "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
# }
#
# html = requests.get(url=url,headers=headers)
# # res= etree.HTML(html.text)
# print(html.text)

import re
a = "setbg('查看完整电话',420,520,'https://www.78gk.net/box.php?part=seecontact_tel&id=381022&tel_base64=MTM2NDM4NTM3MjA=')"
par=re.compile("https:.*?\)")
res=re.findall(par,a)[0].split("')")[0]
print(res)
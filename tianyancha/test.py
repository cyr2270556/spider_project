import requests
import json
start_url = 'https://api9.tianyancha.com/services/v3/search/homePageHotWord'
headers={
"Host":"api9.tianyancha.com",
"Connection":"keep-alive",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
"content-type":"application/json",
"version":"TYC-XCX-WX",
"Referer":"https://servicewechat.com/wx9f2867fc22873452/37/page-frame.html",
"Accept-Encoding":"gzip,deflate,br"

}

# res = requests.get(url=start_url,headers=headers)
# res_dict = json.loads(res.text)
# result_list=res_dict['data']['hotHuman']['resultList']
# for i in result_list:
#     print(i)


res = requests.get(url=start_url,headers=headers)
print(res.json()['data'])
# result_list=res_dict['data']['hotHuman']['resultList']
# for i in result_list:
#     print(i)



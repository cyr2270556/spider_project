#2021/1/11 爬取商标文字信息，获取图片页码
import requests
import json
from TOOLS.mongosave import MongoDB
from TOOLS.md5encode import md5encryption
#改数据库
db = MongoDB('mongodb://localhost', 'cuiworkdb', "Shangbiao_GG-1731")
from Func.fetchJX import FETCH

s = FETCH()
#改url
url = 'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearchDG.html?O56fzBVE=5kGuYaPrUkHH9Lq8YrTHefgypngRP23L4qgXUWGQn1TKi8Yd5igEworl0xfbe_QQgAs_cOt3plSW7uuYJrq7L1WIUpjbSV_Y8jwT7pDt3qBvN3dxHlaivZlvTyYxD3JctgtaJru5MJhZZxGydeS.3ZoIfni9CZxyKko2tQuVGHLbUbVBWout9qOnP1i6mGCnxEGiUea_nSP_3xljf3U6zkgZ.c5DKXAuQiGzZjKcCLOKPsuFP3CgjXwhbt5ESmD3jfvCNBjc.Mtyy4_D_bfDngudJ.DvhsEJGWicOi6eI9.5BhuIoL5WfOPkkmcebfPQXvuh0SBxzitoPdczDRmEvxbzY2c5irpolrybljU4ZbUVkv0X8Dz5Kv38UUvuDfGXI'
#改Cookie
headers={
"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"283",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Cookie":"_gscu_1645064636=76464150vsisqf48; _gscu_2023327167=76464150m8szyi25; _trs_uv=k9wi5ba1_4030_8pj2; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1597140998; UM_distinctid=174ae765669480-09ef6ad0f222cb-4353761-1fa400-174ae76566aa07; goN9uW4i0iKzS=5db92.A0J2CMY23basgx2TZ.mTIJ7lkLr89FeTJ1C0aRMHE_2AokqW2_4RJ42AQplsUcWhHGBKqZ3JYJcp..cRA; __jsluid_h=b6457e19fe1b05edea1f19ada75c9f46; tmas_cookie=2272.7688.15400.0000; 018f9ebcc3834ce269=09b16dacaa2e3b985f2267dc76e5ae8f; JSESSIONID=0000mA5W99E1uXfd1qh0wgqzyqA:1bm112s99; goN9uW4i0iKzT=53cCT8DqzzR9qqqm67L0OCGfXkxa3Eg9kcZgg2BzmN4mJeGvNh.af42XRAU.5pBn6JEBVQW9X7_5Q0c0BLcubFHR3V2NtqqslXLY0Rg.3qvRoSOo.eXYEunrAawqXfJ4OYHTCLen_Z85LNWTB77aJOXfqtOqhlOUMzVD_5wlioEYc22WaLxHAvTwqbtDutolgF8kpTIldeoQJwo89qgNpe0ZOzZwHaaYC3qh7.7bucy3WpAnMVKFV_K_LPWPdL195mAzPq8uiBWY5CRMjmCfU88wyS.H5RFGSvrFx87nTLofgdhXnNMBq1vgUkTx5FYpDxvN5jaQg8eqCoedhokTjYW",
"Host":"wsgg.sbj.cnipa.gov.cn:9080",
"Origin":"http://wsgg.sbj.cnipa.gov.cn:9080",
"Pragma":"no-cache",
"Referer":"http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",
}

#不改
paramters={
"O56fzBVE":"5ioHylbveVMPtuKiT90F3goDPVxIp9QL_d.8t2W2HJPuxqZrOKwd7FqwsDqbo72g3XuScYfBWTufhzKXlQ0SGkUAOgrdbwxaWR0sObQ9Go.oVYepNhPWrNB_cqWx9xvpwsXSxt47NPqCY6g4QdbHBguw7geCh7MwparCW2r1qjhy5xuRaN8A_rOiwbH7Q5G73l0KsQIF_TGTTwRJZ47qxEI0xdWaHviO5hp0DZyXfgkgRedailyAPnI9LKnmQAjMRSeDrxhkPVjIp_eigkEOcN7BT8dkksqlrCA7FnjmT_BToUNsRhJbJejxOLBi4PkNcJVuQjXhOaAuptQKqeTlXhjEF3ZhUrmVC8iszjhyPDVipNuxjQK75WC1MtUXhC48Y"
}

#改annNum，rows
post_data={
"page":"1",
"rows":"20",
"annNum":"1731",
"annType":"TMSDGG",
"tmType":"",
"coowner":"",
"recUserName":"",
"allowUserName":"",
"byAllowUserName":"",
"appId":"",
"appIdZhiquan":"",
"bfchangedAgengedName":"",
"changeLastName":"",
"transferUserName":"",
"acceptUserName":"",
"regName":"",
"tmName":"",
"intCls":"",
"fileType":"",
"totalYOrN":"true",
"appDateBegin":"",
"appDateEnd":"",
"agentName":"",

}
#{"page_no":302,"tm_name":"NASA","ann_type_code":"TMSDGG","tmname":"NASA","reg_name":"PABLOSKY,S.L.",
# "ann_type":"送达公告","ann_num":"1678","reg_num":"G632057","id":"e48b92f76f4c83dc016f5bf06b6b2316",
# "rn":1,
# "ann_date":"2020-01-06","regname":"PABLOSKY,S.L."}
#数据页数加1
for i in range(584):
    post_data["page"] = str(i)
    # res= requests.post(url=url, data=post_data, json=paramters, headers=headers)
    res = s.fetch(url=url, data=post_data, method='post', headers=headers)
    print(res.text)
    try:

        json_obj=json.loads(res.text)
        for item in json_obj["rows"]:
            id = md5encryption(item['reg_num'])
            item['_id'] = id
            item["type"] = ''
            db.mongo_add(item)
    except :
        continue
# print(res.text)
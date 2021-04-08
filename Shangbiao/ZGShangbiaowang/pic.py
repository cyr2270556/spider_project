#2021/1/11 爬取图片url

# import requests
# from time import sleep
# import json
# from TOOLS.mongosave import MongoDB
#
# db = MongoDB('mongodb://localhost', 'cuiworkdb', "Shangbiao_GG-1678")
#
# pic_url = "http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/imageView.html?O56fzBVE=5kh4GeM3E81ApcS2U_k3qv3BYhFVddqMnoWqw5ZclUodLu.0EvDoTtEUEZBte5op.LhORs2ODeNaPSvA5mA9P9VLeTbdY0qM1A85vx6w67x.uk6eWSgQjo6CvvdPwTWWsoscOWyIbVgqogFR0Kyf.ntdYTkQyIW4Kk8BcrvT8mptXWy5vqslBqm6Yy6u_1xUa_zbtt5M.RST9RP6Do_DEj49wkqbcWFLIE8XUeghky2ajN60idwSyVGatD_AbVYEeZZjmCLzuf8ZPCst_Ugtx1MPjhUbzDFfWbxcpQp14sKMYPK0A.qZb8F8atnBaeK6EoU979cyc0ilmHz7tVUCFeCLXRC0r7qo9Q_EnqdghIydO05cPwwWCiGpNN.itB.L7"
#
# pic_headers = {
#     "Accept":"application/json, text/javascript, */*; q=0.01",
#     "Accept-Encoding":"gzip,deflate",
#     "Accept-Language":"zh-CN,zh;q=0.9",
#     "Cache-Control":"no-cache",
#     "Connection":"keep-alive",
#     "Content-Length":"52",
#     "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
#     "Cookie":"_gscu_1645064636=76464150vsisqf48; _gscu_2023327167=76464150m8szyi25; _va_id=5e4adce19f304835.1576464151.1.1576465224.1576464151.; _trs_uv=k9wi5ba1_4030_8pj2; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1597140998; UM_distinctid=174ae765669480-09ef6ad0f222cb-4353761-1fa400-174ae76566aa07; goN9uW4i0iKzS=5db92.A0J2CMY23basgx2TZ.mTIJ7lkLr89FeTJ1C0aRMHE_2AokqW2_4RJ42AQplsUcWhHGBKqZ3JYJcp..cRA; __jsluid_h=b6457e19fe1b05edea1f19ada75c9f46; tmas_cookie=2272.7689.15400.0000; 018f9ebcc3834ce269=3d5227fdd80cd753b97d8d52ee2b1bf0; JSESSIONID=0000uc0XBAf8r-4yI1VjD643pKw:1bm104o7j; arp_scroll_position=601; goN9uW4i0iKzT=5Ud85Pmd6BN9qqqmC6ZAAua189_tOGvkrqUAYuJbjMvFfDL4K6O9GZY8Et2MT_UUSEwrEj7xlHmHze0xSO.2gvlp_fAf_KRlNC2in7M6iuW4uLtrXX4py_az.GMMp0jhJl7wuovGHD2uhuWXnSgnFUBSkYqXa6FBwB9dD6vT1WDidw93CjTJo.9yGQ8guKy44ZHTRWEiN_edjPQ0swRsml.ia_wPuvObMqrIg9t2oAucAN_.Np0H8gtMdAFY804x7Lylvo3C3gDsvpf13Q4WzDAXzAk1v.97kVrP1BRmtMXkc.OHT5Wav_MwBQzvBELK9HHMEpSr8Vb5pAZL4VG3jPP",
#     "Host":"wsgg.sbj.cnipa.gov.cn:9080",
#     "Origin":"http://wsgg.sbj.cnipa.gov.cn:9080",
#     "Referer":"http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html",
#     "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
#     "X-Requested-With":"XMLHttpRequest"
# }
#
# pic_json_que = {
#     "O56fzBVE":"5kh4GeM3E81ApcS2U_k3qv3BYhFVddqMnoWqw5ZclUodLu.0EvDoTtEUEZBte5op.LhORs2ODeNaPSvA5mA9P9VLeTbdY0qM1A85vx6w67x.uk6eWSgQjo6CvvdPwTWWsoscOWyIbVgqogFR0Kyf.ntdYTkQyIW4Kk8BcrvT8mptXWy5vqslBqm6Yy6u_1xUa_zbtt5M.RST9RP6Do_DEj49wkqbcWFLIE8XUeghky2ajN60idwSyVGatD_AbVYEeZZjmCLzuf8ZPCst_Ugtx1MPjhUbzDFfWbxcpQp14sKMYPK0A.qZb8F8atnBaeK6EoU979cyc0ilmHz7tVUCFeCLXRC0r7qo9Q_EnqdghIydO05cPwwWCiGpNN.itB.L7"
# }
#
# pic_data = {
#     "id":"e48b92f76f4c83dc016f5beebb021f08",
#     "pageNum":"",
#     "flag":"1",
# }
# #第四个开始才是nasa
#
# all_data=db.find_all()
# for item in all_data:
#     id=item["_id"]
#     pic_data["pageNum"]=str(item["page_no"])
#     try:
#         res = requests.post(url=pic_url, headers=pic_headers, data=pic_data, json=pic_json_que)
#         print(res.text)
#         res_json = json.loads(res.text)
#         pic_url = res_json["imaglist"][3]
#         print(pic_url)
#     except:
#         continue
#     """
#     myquery = { "alexa": "10000" }
# newvalues = { "$set": { "alexa": "12345" } }
#
# mycol.update_one(myquery, newvalues)
#     """
#     db.mong_find_one_update({"_id":id},{"pic_url":pic_url})
#
#
#
# # for i in range(302, 2262, 20):
# #     pic_data["pageNum"] = i
# #     res = requests.post(url=pic_url, headers=pic_headers, data=pic_data, json=pic_json_que)
# #     res_json = json.loads(res.text)
# #     print(res_json["imaglist"])
# #     sleep(5)
# #
# # text_url='http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearchDG.html?O56fzBVE=5zVw9fXZ4Req4c3hc19IRHrtiKj1OGRe1rF_SXQZxf3GkE1lrN2sslJr6FAg7ndd51EUCiJ_S8EIkR4aIHz9UlSsjjFnD8w_i8lPmGXOxtBURPKmtu2QvRgEdDjrf0yLub4z90UzG3KJmObB5LgWXB6.VOsAzBi.KfVYS2Edf5LdoO3wID_VqAtObwp2pklg7zQp_OoFsu0LMIEQfdAIMzICr.AgXspltnf7FhCrvgxl_pFnjoKEpzZ2PyZ.FAsC9JUZrFJ1nPCoIQzqDdLSkPCKBKzZhcJgBDlW4Ma7.uyHh0IFq1oMbql1QFCXz6DSOEM378TaczqHAfN623H3Ifb0NGqaJIy9IXFWCCu8u7Y_lUHJ8F93QXkgtOWnk9Mfv'
# #
# # text_headers={
# # "Accept":"application/json, text/javascript, */*; q=0.01",
# # "Accept-Encoding":"gzip, deflate",
# # "Accept-Language":"zh-CN,zh;q=0.9",
# # "Cache-Control":"no-cache",
# # "Connection":"keep-alive",
# # "Content-Length": "283",
# # "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
# # # "Cookie":"_gscu_1645064636=76464150vsisqf48; _gscu_2023327167=76464150m8szyi25; _va_id=5e4adce19f304835.1576464151.1.1576465224.1576464151.; _trs_uv=k9wi5ba1_4030_8pj2; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1597140998; UM_distinctid=174ae765669480-09ef6ad0f222cb-4353761-1fa400-174ae76566aa07; 018f9ebcc3834ce269=307cd64d3da74d84b192c7fbed332298; goN9uW4i0iKzS=5db92.A0J2CMY23basgx2TZ.mTIJ7lkLr89FeTJ1C0aRMHE_2AokqW2_4RJ42AQplsUcWhHGBKqZ3JYJcp..cRA; __jsluid_h=b6457e19fe1b05edea1f19ada75c9f46; tmas_cookie=2272.7689.15400.0000; arp_scroll_position=0; JSESSIONID=0000Val4ClB1v2qaHp4KknKydxk:1bm104p42; goN9uW4i0iKzT=5UdFXv2dC..EqqqmCCeO.7qw_1CYUm2E0ikJ89hLkNlNhwhhBo0h5a3sh3ieOh3itkB59QvN5qCfHTK4_UJM8GMEYxl2j15kCGStNQykMxHRugT6AjTh1SSB40HyD_smOTyYm2hrTxZFLgnrT0ZJnKL3zKdVwdSe4CddgaiQAhsob7Tw4HLQ8NxdNdZiy8IOkJwk4IM.fQr34QakSXX8D5ZFR6hNw8NB3A.6_Aml8xFYdglpjk210OEYxkcYdaaZW5Pqo9VoXsK5hxA83a3uxXuDLuXFFXHgQeVIn2aORxmXriEIAdl2.B2Vr04HQhlpZyotwTS54eNezn7XIHF4pxg",
# # "Cookie":"",
# # "Host":"wsgg.sbj.cnipa.gov.cn:9080",
# # "Origin":"http://wsgg.sbj.cnipa.gov.cn:9080",
# # "Pragma":"no-cache",
# # "Referer":"http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=",
# # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
# # "X-Requested-With":"XMLHttpRequest",
# #
# # }
# #
# # text_data={
# # "page":"1",
# # "rows":"20",
# # "annNum":"1678",
# # "annType":"TMSDGG",
# # "tmType":"",
# # "coowner":"",
# # "recUserName":"",
# # "allowUserName":"",
# # "byAllowUserName":"",
# # "appId":"",
# # "appIdZhiquan":"",
# # "bfchangedAgengedName":"",
# # "changeLastName":"" ,
# # "transferUserName":"",
# # "acceptUserName":"",
# # "regName":"",
# # "tmName":"",
# # "intCls":"",
# # "fileType":"",
# # "totalYOrN":"true",
# # "appDateBegin":"",
# # "appDateEnd":"",
# # "agentName":"",
# # }
# #
# # text_json_que={
# #     "O56fzBVE":"5zVw9fXZ4Req4c3hc19IRHrtiKj1OGRe1rF_SXQZxf3GkE1lrN2sslJr6FAg7ndd51EUCiJ_S8EIkR4aIHz9UlSsjjFnD8w_i8lPmGXOxtBURPKmtu2QvRgEdDjrf0yLub4z90UzG3KJmObB5LgWXB6.VOsAzBi.KfVYS2Edf5LdoO3wID_VqAtObwp2pklg7zQp_OoFsu0LMIEQfdAIMzICr.AgXspltnf7FhCrvgxl_pFnjoKEpzZ2PyZ.FAsC9JUZrFJ1nPCoIQzqDdLSkPCKBKzZhcJgBDlW4Ma7.uyHh0IFq1oMbql1QFCXz6DSOEM378TaczqHAfN623H3Ifb0NGqaJIy9IXFWCCu8u7Y_lUHJ8F93QXkgtOWnk9Mfv"
# # }
# #
# #
# # res = requests.post(url=text_url,headers=text_headers,data=pic_data,json=text_json_que)
# # print(res.text)


####2021/1/8 爬取对应数据图片url


import requests
from time import sleep
import json
from Func.client import MongoDB
from Func.fetchJX import FETCH
s = FETCH()
#改数据库
db = MongoDB('mongodb://localhost', 'cuiworkdb', "Shangbiao_GG-1731")
#改url
url = "http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/imageView.html?O56fzBVE=5cRVmWcgP6gC.1ulRszzI2_aOlP1jkNH0mxnPtgkE73P.1rSAtlAU1rHW64aHQoXm471Fzq7QOzRfVJiLnarbCbBAjmRHPnmNTUqx.Bfa6RWoAiipN6HKjl5E3Nb6Jp_LaGu5Dr0x1V4f2AsDjRza2LmDcNsd62msQ6SzqM646fK0XNFf.KzqSrexNQiIbLTdcX2wDPfCad.6G6Y4Pq28hw_OMDoIYVwZSvwH.emWD5UAVTbKi.mblyWCBYJOMZx5OMbUMWr05.V6JtgmG.usyr3_8OtVx8yHqisK54faJIdqZ5ofaDE4r6mjkZiGtqZZ96H_kqpPDS1WOjZMSlQGqQal8YnoPPDasrJ5lPkWyphiagHypaYQfoBfWUc3idLO"

#改cookie
pic_headers = {
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip,deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Content-Length":"52",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"_gscu_1645064636=76464150vsisqf48; _gscu_2023327167=76464150m8szyi25; _trs_uv=k9wi5ba1_4030_8pj2; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1597140998; UM_distinctid=174ae765669480-09ef6ad0f222cb-4353761-1fa400-174ae76566aa07; goN9uW4i0iKzS=5db92.A0J2CMY23basgx2TZ.mTIJ7lkLr89FeTJ1C0aRMHE_2AokqW2_4RJ42AQplsUcWhHGBKqZ3JYJcp..cRA; __jsluid_h=b6457e19fe1b05edea1f19ada75c9f46; tmas_cookie=2272.7688.15400.0000; 018f9ebcc3834ce269=09b16dacaa2e3b985f2267dc76e5ae8f; arp_scroll_position=0; goN9uW4i0iKzT=53cCT8DqzzRLqqqm67z1U8qKZLtDgJCjEPobnFeBoFOQEkx_Gy09SZfAajrh2D40V2DJdi_T6Yxefkk.TyC5jkWKRfroyI0Ty8DNR0q2gea8MtkfUvIUVuyOffOLFIesbBvkJ4FVJn0c2XCNKuJKF5uWYYxN.9fe9K5lzUFILMY4E2DDUzrR2u3s2n5yMTLQ3QYDyAIEHcwh9210LUxxFmRFBxLVwWtAcBV_6cTdtf3pc22FM8A8bg8AGXagoEJRxfL.Lj2tq4BK8Li.zsiPB6R; JSESSIONID=0000P2s6vou1xkNAr0uRAjbsxE9:1bm112s99",
    "Host":"wsgg.sbj.cnipa.gov.cn:9080",
    "Origin":"http://wsgg.sbj.cnipa.gov.cn:9080",
    "Referer":"http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
}
#不改
pic_json_que = {
    "O56fzBVE":"5PRYIPHwao2wTbpLKwSfk_Zh_bs2BrqEZVRte2iiPpxsAb6pmV2M_wBOKuGnWUrk5o1RN5Xqn7yxcKUUxW.nPvg138z.b1F1nQVEnmjcHC0WapfNRo31Hi2rIx9exsaIdqlv.AgQW1LuGOVrBfSPrGsDbA5yLIWgtPE3n5mH5BDxmflTLmt0WaQRyIE89FpmLotL4nyLe1JIXktE030K6C5PcM9Av0OwjCP4yC30D6AIotUwNMV0cRe6Z50ZC7TWg.IupA1S2rKMANapgkLt7cVztj9T8215YrrzcopenfuoBc00GVuHfjmm6l1QSBxko45_dGhMwH7HHPyFC2LvjQikmMmILgCP6hkw7YM0S_jiXg5EQe5SOk418paE_KbK4"
}
#改id
pic_data = {
    "id":"e48b92f1776fbff70177711dab173aac",
    "pageNum":"1",
    "flag":"1",

}

# res = requests.post(url=pic_url, headers=pic_headers, data=pic_data, json=pic_json_que)
# print(res.text)
#第四个开始才是nasa

# all_data=db.find_all()


# for item in all_data:
#     id=item["_id"]
#     # pic_data["pageNum"]=str(item["page_no"])
#     pic_data["pageNum"]="303"
#     print(pic_data)
#     res=s.fetch(url=pic_url, headers=pic_headers, data=pic_data, method="post")
#     # res = requests.post(url=pic_url, headers=pic_headers, data=pic_data, json=pic_json_que)
#     res_json = json.loads(res.text)
#     pic_url = res_json["imaglist"][3]
#     print(pic_url)
#
#     db.mong_find_one_update({"_id":id},{"pic_url":pic_url})

#改页数+1
for i in range(5821):
    pic_data["pageNum"] = str(i)
    print(pic_data)
    # res = s.fetch(url=pic_url, headers=pic_headers, data=pic_data, method="post")
    res = s.fetch(url=url, headers=pic_headers, data=pic_data,method="post")
    # res = requests.post(url=url, headers=pic_headers, data=pic_data, json=pic_json_que)

    print(res)
    print('resURL:',res.url)
    res_json = json.loads(res.text)
    pic_url = res_json["imaglist"][3]
    db.mong_find_many_updata({"page_no": i}, {"pic_url":pic_url})






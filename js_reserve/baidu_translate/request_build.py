#百度翻译js逆向

import requests
from lxml import etree
from js_reserve.baidu_translate.test import get_sign
import json
request_url='http://fanyi.baidu.com/basetrans'

headers={
"Accept":"*/*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cache-Control": "no-cache",
"Connection": "keep-alive",
"Content-Length": "138",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Cookie": "PSTM=1557906769; BIDUPSID=EB232CE97FC174A2B7ECB6407A42718E; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=3E8AD66FD1228FCCD1B17F015045FBC3:FG=1; __yjs_duid=1_84e7f416261f06a93894b4e98ac7e33e1611562070212; H_WISE_SIDS=107319_110085_127969_131423_144966_156286_156926_161083_162372_162898_163274_163389_163509_163567_163568_163928_164163_164297_164326_164955_165133_165136_165328_166148_166255_166434_166476_166885_167086_167165_167296_167324_167397_167403_167443_167536_167744_167944_168033_168099_168193_168235_168403_168540_168551_168567_168572_168618_168719_168734_168768_168909_168914; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDSFRCVID=TQuOJexroG3VnU3eyyKzudblcLweG7bTDYLEOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJAj_D-btK03H48k-4QEbbQH-UnLqModLgOZ04n-ah05_P5FjtoGQ4-N5fOa2Pte32DJLK5m3UTdfh76Wh35K5tTQP6rLf6Ob264KKJxbnckMqnaj-5dKxo-hUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCICejKbDjoM5pJfetJa2RAqoTr854-3SncJXU6qLT5Xjb-etq3n565UQPJa5noSHIoGhTQTyl0njxQytUj8KbcvLKoktt5YqD3S2fonDh8ZbG7MJUntHG5H2InO5hvvob3O3M7bDMKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQbG_EJ6nhKCo8B6rtKRTffjrnhPF3DtuvXP6-hnjy3b7pWfKb54TdDpRGb-5S-UAWbttf5q3RymJ42nnzX-nhJhQg3634y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrMDb5tWMT-MTryKKOCafK5etTwyP6hb-Dj-PvfKx-fKHnRhlRNB-3iV-OxDUvnyxAZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDMJ9LUkqW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCvDqTrP-trf5DCShUFsLpotB2Q-XPoO3KO4DxKRbJrBynI0bM5Q5M7f5mkf3fbgylRp8P3y0bb2DUA1y4vpBtQmJeTxoUJ2-KDVeh5Gqfo15-0ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHjL5j6j03f; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1612237898,1612237902,1612245783,1612245825; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1612245825; ab_sr=1.0.0_ODQ0YmRlODdiNDNiOGU4MzNlODRlY2Q4NWYzZDUwNzc1MzM4YzdhMWZjNWM0YzU1NmMzODdlODc1YmM2NWQyZTFjOTRmOWQ5YjA2M2YxMzdmNDk5ZTA3YjVlYWJiNzdk; arp_scroll_position=0; delPer=0; PSINO=6; BDSFRCVID_BFESS=TQuOJexroG3VnU3eyyKzudblcLweG7bTDYLEOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJAj_D-btK03H48k-4QEbbQH-UnLqModLgOZ04n-ah05_P5FjtoGQ4-N5fOa2Pte32DJLK5m3UTdfh76Wh35K5tTQP6rLf6Ob264KKJxbnckMqnaj-5dKxo-hUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCICejKbDjoM5pJfetJa2RAqoTr854-3SncJXU6qLT5Xjb-etq3n565UQPJa5noSHIoGhTQTyl0njxQytUj8KbcvLKoktt5YqD3S2fonDh8ZbG7MJUntHG5H2InO5hvvob3O3M7bDMKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQbG_EJ6nhKCo8B6rtKRTffjrnhPF3DtuvXP6-hnjy3b7pWfKb54TdDpRGb-5S-UAWbttf5q3RymJ42nnzX-nhJhQg3634y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrMDb5tWMT-MTryKKOCafK5etTwyP6hb-Dj-PvfKx-fKHnRhlRNB-3iV-OxDUvnyxAZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDMJ9LUkqW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCvDqTrP-trf5DCShUFsLpotB2Q-XPoO3KO4DxKRbJrBynI0bM5Q5M7f5mkf3fbgylRp8P3y0bb2DUA1y4vpBtQmJeTxoUJ2-KDVeh5Gqfo15-0ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHjL5j6j03f; BA_HECTOR=0k8h0121808081a5sn1g1huqe0r",
"Host": "fanyi.baidu.com",
"Origin": "https://fanyi.baidu.com",
"Pragma": "no-cache",
"Referer": "https://fanyi.baidu.com/?aldtype=16047",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"
}

# cookie2="PSTM=1557906769; BIDUPSID=EB232CE97FC174A2B7ECB6407A42718E; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=3E8AD66FD1228FCCD1B17F015045FBC3:FG=1; __yjs_duid=1_84e7f416261f06a93894b4e98ac7e33e1611562070212; H_WISE_SIDS=107319_110085_127969_131423_144966_156286_156926_161083_162372_162898_163274_163389_163509_163567_163568_163928_164163_164297_164326_164955_165133_165136_165328_166148_166255_166434_166476_166885_167086_167165_167296_167324_167397_167403_167443_167536_167744_167944_168033_168099_168193_168235_168403_168540_168551_168567_168572_168618_168719_168734_168768_168909_168914; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; delPer=0; PSINO=6; BDRCVFR[86pcH-5hBUC]=uk68N_1oXw_uv4MrHc8mvqV; BAIDUID_BFESS=143F31B4E67E0C7A62AC9E3D39A22D1D:FG=1; BDRCVFR[VBH4JnM-Vd0]=uk68N_1oXw_uv4MrHc8mvqV; BCLID=11436347761787404691; BDSFRCVID=1mDOJexroG3VnU3eyLoLudblcLweG7bTDYLELhM_xuxFdV0VJeC6EG0Pts1-dEu-EHtdogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRKOoILKfIt3H48k-4QEbbQH-UnLqKrD3gOZ04n-ah05SCJJM4oGDDuF5fOa2PtHW23M_bcm3UTKsq76Wh35K5tTQP6rLf6fQej4KKJxbInfOUJD0-5UyfCjhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCDwe50-j6vQepJf-K6DKKAX3b7Ef-Omsl7_bJ7KhUby3G3matQI3jra-ITTLnFKOpvTjP6xQhFXQtr3tnFtXKkq0nrcQqrbSl6HQT3m55kOyn3lQPjRWmoQWb3cWKJJ8UbSjxRPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKeJTKJtbAfVbobHJoHjJbGq4bohjPFBn39BtQO-DOxoM7a2D5qVqQTXRof-4ASDPJutn-tQgnk2PbvbMnmqPtRXMJkXhKN2hJC0x-jLTnBaD5dQCbD8-oqetnJyUnQbPnnBT5i3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CFXJDIKMIDlenJb5ICS-xuetj8XaDTJVM3_0h7keq8CD6O6DTK73Mo8LbOjbCnaWn8-bRAaEpc2y5jHhT0Y2f-qXn-HBJrt24D5WPTpsIJM34DWbT8U5eckbfAOaKviaMnjBMb1fIJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6oMbxQXh4FXKD600PK8Kb7VbIjzQMnkbJkXhPteLt6PtKT82n71bRbDDbOs5PonjPD7Qbrr0x73BGOOL4nI5UL2SlcNLTjpQT8r5h-De434b4j4aPbeab3vOIJTXpO1jxPzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqtJHKbDf_CDb3J; BCLID_BFESS=11436347761787404691; BDSFRCVID_BFESS=1mDOJexroG3VnU3eyLoLudblcLweG7bTDYLELhM_xuxFdV0VJeC6EG0Pts1-dEu-EHtdogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tRKOoILKfIt3H48k-4QEbbQH-UnLqKrD3gOZ04n-ah05SCJJM4oGDDuF5fOa2PtHW23M_bcm3UTKsq76Wh35K5tTQP6rLf6fQej4KKJxbInfOUJD0-5UyfCjhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCDwe50-j6vQepJf-K6DKKAX3b7Ef-Omsl7_bJ7KhUby3G3matQI3jra-ITTLnFKOpvTjP6xQhFXQtr3tnFtXKkq0nrcQqrbSl6HQT3m55kOyn3lQPjRWmoQWb3cWKJJ8UbSjxRPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKeJTKJtbAfVbobHJoHjJbGq4bohjPFBn39BtQO-DOxoM7a2D5qVqQTXRof-4ASDPJutn-tQgnk2PbvbMnmqPtRXMJkXhKN2hJC0x-jLTnBaD5dQCbD8-oqetnJyUnQbPnnBT5i3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CFXJDIKMIDlenJb5ICS-xuetj8XaDTJVM3_0h7keq8CD6O6DTK73Mo8LbOjbCnaWn8-bRAaEpc2y5jHhT0Y2f-qXn-HBJrt24D5WPTpsIJM34DWbT8U5eckbfAOaKviaMnjBMb1fIJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6oMbxQXh4FXKD600PK8Kb7VbIjzQMnkbJkXhPteLt6PtKT82n71bRbDDbOs5PonjPD7Qbrr0x73BGOOL4nI5UL2SlcNLTjpQT8r5h-De434b4j4aPbeab3vOIJTXpO1jxPzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqtJHKbDf_CDb3J; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1611284697,1611901185,1612237898,1612237902; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1612237908; ab_sr=1.0.0_YzlhY2RhMmVlYjlhNzE1ODdkZDFjMzVkODc5YjI3ZjlhODEwMDliOTUwMWE2MTZkM2U3ODRmZDc0MjgwOWUxZmU3NmE4NTRmNThiZTQxZWM2OTVjNzdmMzMwNWE5ZGVm; arp_scroll_position=0"

form_data = {
"from": "en",
"to": "zh",
"query": "English",
"transtype": "realtime",
"simple_means_flag": "3",
"sign": get_sign(input("输入要翻译的单词")),
"token": "69fb5adf239f6b11e32b1efa16aa5bfe",
"domain": "common"
}

html = requests.post(url=request_url,headers=headers,data=form_data)
print(html.text)
res = etree.HTML(html.text)
print(res)

#给没有flag字段的表添加flag=1，表应该是已推送的表，后续做增量爬取，（只做第一次）
#给已经推送的表改变flag=1
from Func.client import MongoDB

#只做一次
m = MongoDB('mongodb://localhost', 'cuiworkdb', '9guakao_zhengzhou')
m.add_field_for_all()

#改变flag=0为flag=1
m = MongoDB('mongodb://localhost', 'cuiworkdb', 'jianzhutong_beijing')
m.change_flag()




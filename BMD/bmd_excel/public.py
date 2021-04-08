#白名单通用api
#每日BMD任务更改日期（mongo集合名和文件位置）

from TOOLS.mongosave import MongoDB
db = MongoDB('mongodb://localhost', 'cuiworkdb', 'BMD20210205-chengdu')


Format_code = {

    "项目": "BUS_YT_XM",
    "创业发展": "BUS_YT_CY",
    "资质": "BUS_YT_ZZ",
    "互联网": "BUS_YT_HLW",
    "财税": "BUS_YT_CS",
    "会计": "BUS_YT_KJ",
    "金融发展": "BUS_YT_JRFZ",
    "法律": "BUS_YT_FL",
    "培训（大卓商学院）": "BUS_YT_DZSXY",
    "综合": "BUS_YT_ZH",
    "项目(知产)": "BUS_YT_ZSCQ",
    "品牌": "BUS_YT_PP",
    "人事外包": "BUS_YT_RSWB",
    "装饰": "BUS_YT_ZS",
    "融资": "BUS_YT_DK",
    "商标版权": "BUS_YT_SBBQ",
    "专利项目": "BUS_YT_ZLXM",
    "巨方地产(禁用)": "BUS_YT_JFDC",
    "认证": "BUS_YT_TXRZ",
    "创新": "BUS_YT_CX",
    "网点交易": "BUS_YT_WDJY"
}

city = {
    "北京": "北京市",
    "重庆": "重庆市",
    "石家庄": "河北省",
    "郑州": "河南省",
    "广州": "广东省",
    "深圳": "广东省",
    "东莞": "广东省",
    "佛山": "广东省",
    "武汉": "湖北省",
    "宜昌": "湖北省",
    "上海": "上海市",
    "成都": "四川省",
    "杭州": "浙江省",
    "长沙": "湖南省",
}


document_address = r"G:\c_spider_work_project\qcc_excel\未清洗文件\今日文件（导出请清空文件夹）"
target_city = '成都'
Format = '资质'

shiyebu_ID = ''

bumeng_ID = ''

zhongxing_ID = ''




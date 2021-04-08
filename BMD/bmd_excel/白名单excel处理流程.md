# 白名单excel处理流程

1.从企查查网站https://www.qcc.com/?utm_source=baidu1&utm_medium=cpc&utm_term=pzsy
高级查询选择省份地区（根据需求），年限默认1-3年，在业/存续，有手机号码，查出excel表格，（时间从当前时间往前推3年，重命名excel文件名）

2.使用BMD文件内bmd3.py 将文件存入暂存mongo库（随便哪个都行只要不是推数据的库，存在本地mongo集群），打开Navicat连接138，选择tes库右键导入向导...（未完待续）。

向导csv文件如何生成？：

```
mongoexport -d cuitestdb -c testdb -o D:\mongodb\data\db1.csv --type csv -f "_id,companyName,compantTel"  
```

   这段代码从mongo文件处cmd执行  E:\Program Files\MongoDB\bin

```
mongoexport -d 暂存本地库名-c 暂存本地表名-o D:\mongodb\data\db1.csv --type csv -f "_id,companyName,compantTel" 
```

（_id 必带，companyName等根据需求给，按照mongo存储的字段名来写）
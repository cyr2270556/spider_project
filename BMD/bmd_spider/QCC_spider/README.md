自动化抓取网页源代码
绕过反爬不向网页发起请求
模拟人为操作（基本不可能出现验证码反爬）

如何操作：
1.开启目标网页，打开网页源代码页面
2.开启pycharm 到代码执行位置
3.在run.py文件传入爬取页数参数，xpath规则参数，等待程序进行爬取即可
4.注意事项：保证在c盘文档位置没有test.txt文件，alt+table必须能够
切换到目标源代码页面

缺点：  1.在执行程序时电脑无法执行其他操作
        2.网页源代码没有的数据无法获得
        3.可能速度较慢（待测试）
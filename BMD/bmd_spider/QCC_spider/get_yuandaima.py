# 自动化脚本获取网页源代码转成txt文件

# 源代码网址view-source:https://www.qcc.com/search_adsearchmultilist?p=1
from pykeyboard import *
from pymouse import *
from time import sleep
from parse_txt import parse
from public import xpath_rule1, xpath_rule2, xpath_rule3


# 一页操作
# 程序执行alt+table 一次 切换到浏览器
# ctrl+U查看网页源代码
# ctrl + A 全选
# ctrl + c 复制
# window 输入txt 回车 打开一个txt
# ctrl +v 粘贴
# ctrl +s 保存 输入 test 回车 文件保存
# 调用处理
# alt + table 切换回浏览器（待观察，好像是一次）
# ctrl+ 1 切换到目标页面

# 翻页操作
# F6 定位到地址栏
# 向右键 + 删除键 准备改变页码数
# 写入页码数 + 回车跳转下一页

# 循环上述操作

# 封装未完成，翻页规则不可复用

def get_html(num):
    page = 2
    while page <= num:
        # 鼠标对象
        sleep(0.5)
        m = PyMouse()
        # 键盘对象
        k = PyKeyboard()

        # 1
        k.press_key(k.alt_key)
        k.tap_key(k.tab_key)
        k.release_key(k.alt_key)
        sleep(0.2)

        # 2
        k.press_key(k.control_key)
        k.tap_key('u')
        k.release_key(k.control_key)
        sleep(0.2)
        # 3
        k.press_key(k.control_key)
        k.tap_key('a')
        k.release_key(k.control_key)
        sleep(0.2)

        # 4
        k.press_key(k.control_key)
        k.tap_key('c')
        k.release_key(k.control_key)
        sleep(0.2)
        # 5
        k.press_key(k.windows_l_key)
        k.release_key(k.windows_l_key)
        sleep(0.2)
        k.type_string("txt")
        sleep(0.2)
        k.press_key(k.enter_key)
        k.release_key(k.enter_key)
        sleep(0.2)

        # 6
        k.press_key(k.control_key)
        k.tap_key('v')
        k.release_key(k.control_key)
        sleep(0.2)
        # 7
        k.press_key(k.control_key)
        k.tap_key('s')
        k.release_key(k.control_key)
        sleep(0.2)
        k.type_string("test")
        k.press_key(k.enter_key)
        k.release_key(k.enter_key)
        sleep(0.2)
        # 8右下角的baiwindows徽标键+R ；输入 tskill notepad 然后回车  或者alt+f4关闭当前窗口（谨慎）
        # k.press_key(k.alt_key)
        # k.tap_key(k.function_keys[4])
        # k.release_key(k.alt_key)

        k.press_key(k.alt_key)
        k.tap_key(k.function_keys[4])
        k.release_key(k.alt_key)

        sleep(1)

        parse(xpath_rule1, xpath_rule2, xpath_rule3)

        # k.press_key(k.alt_key)
        # k.tap_key(k.tab_key)
        # k.release_key(k.alt_key)
        sleep(2)
        # k.press_key(k.alt_key)
        # k.tap_key(k.tab_key)
        # k.release_key(k.alt_key)

        # 查看结果正式环境注释掉
        # sleep(2)

        # 10
        # sleep(5)
        sleep(0.2)
        k.tap_key(k.function_keys[6])
        sleep(0.2)
        k.tap_key(k.right_key)
        k.tap_key(k.backspace_key)
        sleep(0.2)
        k.type_string(str(page))
        sleep(0.2)
        k.tap_key(k.enter_key)

        page += 1
        sleep(1)

        k.press_key(k.alt_key)
        k.tap_key(k.tab_key)
        k.release_key(k.alt_key)
        sleep(0.2)
# k.tap_key(k.function_keys[5])  # Tap F5
# k.tap_key(k.numpad_keys['Home'])  # Tap 'Home' on the numpad
# k.tap_key(k.numpad_keys[5], n=3)  # Tap 5 on the numpad, thrice

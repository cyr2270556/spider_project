"""
两个界面怎么相互跳转
"""

def login():
    # 二级界面
    while True:
        print("\n=========== 查词界面 ============")
        print(" 1.查单词   2.历史记录   3.注销")
        print("================================")

        cmd = input("请输入命令:")
        if cmd == "1":
            pass
        elif cmd == "2":
            pass
        elif cmd == "3":
            break
        else:
            print("请输入正确指令")

while True:
    print("\n======== 登录界面 =========")
    print(" 1.注册   2.登录   3.退出")
    print("==========================")

    cmd = input("请输入命令:")
    if cmd == "1":
        pass
    elif cmd == "2":
        login()
    elif cmd == "3":
        pass
    else:
        print("请输入正确指令")






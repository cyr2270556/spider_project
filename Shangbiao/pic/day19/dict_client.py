"""
dict 客户端

* 发起请求
* 获取数据进行展示
"""

from socket import *
import sys

# 服务端地址
ADDR = ("127.0.0.1",8888)

# 发起注册
def do_register(sockfd):
    while True:
        name = input("Name:")
        passwd = input("Password:")

        if ' ' in name or ' ' in passwd:
            print("用户名或者密码不许有空格")
            continue

        passwd_ = input("Again:")
        if passwd != passwd_:
            print("两次密码不一致")
            continue

        # 发送请求
        msg = "R %s %s"%(name,passwd)
        sockfd.send(msg.encode())
        # 等待反馈
        result = sockfd.recv(128).decode()
        if result == 'OK':
            print("注册成功")
        else:
            print("注册失败")
        return

# 发起登录
def do_login(sockfd):
    name = input("Name:")
    passwd = input("Password:")

    # 发送请求
    msg = "L %s %s"%(name,passwd)
    sockfd.send(msg.encode())
    # 等待反馈
    result = sockfd.recv(128).decode()
    if result == 'OK':
        print("登录成功")
        login(sockfd,name) # 登录成功的情况下进入二级界面
    else:
        print("登录失败")

# 查单次
def do_query(sockfd,name):
    while True:
        word = input("单词:")
        if word == '##':
            break
        msg = "Q %s %s"%(name,word)
        sockfd.send(msg.encode())
        # 接收结果 查到了接收解释 查不到接收Not Found
        result = sockfd.recv(1024).decode()
        print("%s : %s"%(word,result))

# 查历史记录
def do_history(sockfd,name):
    msg = "H "+name
    sockfd.send(msg.encode())
    # 客户端无法确定历史记录数量
    while True:
        # 每次接收一条历史记录
        data = sockfd.recv(1024).decode()
        if data == '##':
            break
        print(data)

# 二级界面   处于登录状态 xxx登录了
def login(sockfd,name):
    while True:
        print("""
        =========== 查词界面 ============
         1.查单词   2.历史记录   3.注销
        ======================= 用户:%s ==
        """%name)
        cmd = input("请输入命令:")
        if cmd == "1":
            do_query(sockfd,name)
        elif cmd == "2":
            do_history(sockfd,name)
        elif cmd == "3":
            break
        else:
            print("请输入正确指令")

# 启动函数
def main():
    # 创建套接字
    sockfd = socket()
    sockfd.connect(ADDR)

    # 一级界面
    while True:
        print("""
        ======== 登录界面 =========
         1.注册   2.登录   3.退出
        ==========================
        """)
        cmd = input("请输入命令:")
        if cmd == "1":
            do_register(sockfd)
        elif cmd == "2":
            do_login(sockfd)
        elif cmd == "3":
            sockfd.send(b"E")
            sys.exit("谢谢使用")
        else:
            print("请输入正确指令")

if __name__ == '__main__':
    main()
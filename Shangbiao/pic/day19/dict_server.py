"""
dict 服务端

* 接收请求
* 处理逻辑
* 给客户端反馈内容
"""

from socket import *
from multiprocessing import Process
from signal import *
import sys
from dict_db import *
from time import sleep

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

# 数据库链接 (父进程)
db = Database()

# 处理注册
def do_register(connfd,name,passwd):
    if db.register(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')

# 处理登录
def do_login(connfd,name,passwd):
    if db.login(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')

# 处理查询单次
def do_query(connfd,name,word):
    db.insert_history(name,word) # 插入历史记录

    mean = db.query(word) # 返回单词解释
    connfd.send(mean.encode())

# 历史记录
def do_history(connfd,name):
    # data ->((name,word,time),(),())
    data = db.history(name)
    for i in data:
        # i-->(name,word,time)
        msg = "%s    %s   %s"%i
        connfd.send(msg.encode())
        sleep(0.1) # 防止粘包
    connfd.send(b'##')  # 历史记录发送完了


# 处理客户端请求
def handle(connfd):
    # 在各自子进程中创建游标,方式相互影响
    db.create_cursor()
    # 循环接收请求,分情况讨论
    while True:
        data = connfd.recv(1024).decode()
        tmp = data.split(' ')
        if not data or tmp[0] == 'E':
            # 客户端退出,结束子进程
            break
        elif tmp[0] == "R":
            # tmp --> [R,name,passwd]
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] == "L":
            # tmp --> [L,name,passwd]
            do_login(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            # tmp --> [Q,name,word]
            do_query(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'H':
            # tmp --> [H,name]
            do_history(connfd,tmp[1])
    # 关闭这个 进程对应的游标 和 连接套接字
    db.cur.close()
    connfd.close()

# 启动函数,搭建网络
def main():
    # 创建tcp 套接字
    sockfd = socket()
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # 处理僵尸
    signal(SIGCHLD,SIG_IGN)

    print("Listen the port %d"%PORT)
    while True:
        try:
            connfd,addr = sockfd.accept()
            print("Connect from ",addr)
        except KeyboardInterrupt:
            sockfd.close()
            db.close() # 关闭数据库
            sys.exit("服务端退出")

        # 为客户端创建新的进程
        p = Process(target=handle,args=(connfd,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()
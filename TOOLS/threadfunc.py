# 线程api
# ？？？待写
from threading import Thread


def start_thread(targetfunc, threadnum, *args):
    """
    :param targetfunc: 线程目标函数
    :param threadnum: 开启线程数
    :param args: 目标函数参数
    :return:
    """
    Args = args
    print(Args)
    thread_list = []
    for tnum in range(1, threadnum + 1):
        t = Thread(target=targetfunc, args=Args)
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()

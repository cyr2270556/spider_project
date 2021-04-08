"""
dict 数据库处理模块

* 根据 服务端在处理过程中的需求 进行数据的处理
"""
import pymysql

class Database:
    def __init__(self):
        self.db = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = '123456',
            database = 'dict',
            charset = 'utf8')

    def create_cursor(self):
        self.cur = self.db.cursor()

    def close(self):
        # 关闭
        self.db.close()

    ########  根据服务端需求写函数 #######
    def register(self,name,passwd):
        sql = "select name from user where name=%s;"
        self.cur.execute(sql,[name])
        r = self.cur.fetchone() # (name,) ()
        if r:
            return False # 不允许注册

        # 插入该用户
        sql = "insert into user (name,passwd) values (%s,%s);"
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True # 注册了 用户
        except:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        sql = "select name from user where binary name=%s and passwd=%s;"
        self.cur.execute(sql, [name,passwd])
        r = self.cur.fetchone()  # (name,) ()
        # 如果能够查询到则可以登录
        if r:
            return True
        else:
            return False

    def query(self,word):
        sql = "select mean from words where word=%s;"
        self.cur.execute(sql,[word])
        r = self.cur.fetchone() # 可能查询不到 (mean,)
        if r:
            return r[0]
        else:
            # 没有查到
            return "Not Found"

    def insert_history(self,name,word):
        sql="select id from user where name=%s;"
        self.cur.execute(sql,[name])
        # 获取这个用户的id值
        user_id = self.cur.fetchone()[0]

        # 插入历史记录
        sql = "insert into hist (word,user_id) values (%s,%s);"
        try:
            self.cur.execute(sql,[word,user_id])
            self.db.commit()
        except:
            self.db.rollback()

    def history(self,name):
        # name  word  time
        sql = "select name,word,time " \
              "from user left join hist " \
              "on user.id = hist.user_id " \
              "where name=%s " \
              "order by time desc " \
              "limit 10;"
        self.cur.execute(sql,[name])
        # ((name,word,time),(),())
        return self.cur.fetchall()

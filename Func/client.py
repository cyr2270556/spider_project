from pymongo import MongoClient
import time

from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError


class MongoDB(object):
    """
    输入一个数据库链接地址、数据库名称（字符串）、collection名称（字符串），不存在则创建
    """
    def __init__(self, uri, db, collection, pool_size=100):
        self._client = MongoClient(uri, maxPoolSize=pool_size)
        self.db = db
        self.collection = collection
        self.wait = time.sleep(2)

    # get /creat a mongo database
    def get_database(self):
        if self._client:
            return self._client.get_database(self.db)
        else:
            raise Exception("MongoClient connection failed")

    # get /creat a mongo collection
    def get_collection(self):
        return self.get_database().get_collection(self.collection)

    def mongo_add(self, dic):
        try:
            self.get_collection().insert_one(dic)
            print('%s 插入成功 !!!!' )

        except DuplicateKeyError as e:

            print('数据重复，已经忽略')

        except ServerSelectionTimeoutError:
            print('MongoDB连接出错，等待重试中……')
            self.wait()
            return self.get_collection().insert_one(dic)

    def mongo_addmany(self, dics):
        self.get_collection().insert_many(dics)

    def mongo_find(self, dic):
        #查找特定字段+值的全部数据
        return self.get_collection().find(dic)

    def mongo_find_one(self, dic):
        return self.get_collection().find_one(dic)

    def mongo_find_company(self,companyName):
        return self.get_collection().find({"companyName":companyName})

    def mongo_update(self, filters, updater):
        self.get_collection().update(filters, {"$set": updater})
        print('插入成功----%s' % filters['_id'])

    def mong_find_one_update(self, filters, updater):
        self.get_collection().find_one_and_update(filters, {"$set": updater})

    def mong_find_many_updata(self,filters, updater):
        self.get_collection().update_many(filters, {"$set": updater})

    # delete a database
    def mongo_deldb(self):
        self._client.drop_database(self.db)

    # delete a collection
    def mongo_delcol(self):
        self.get_database().drop_collection(self.collection)

    # delete all documents
    def mongo_delall(self):
        self.get_collection().remove()

    # delete a document
    def mongo_delone(self, dic):
        self.get_collection().remove(dic)

    def distinct(self, dic):
        self.get_collection().distinct(dic)

    def close(self):
        self._client.close()

    def save_data(self,datadict):
        #传入一个字典存储在mongo
        self._client.insert_one(datadict)
    def find_all(self):

        return self.get_collection().find({} , no_cursor_timeout=True)

    def find_many(self,key,value):

        return self.get_collection().find({key:value},no_cursor_timeout = True)

    def __find_one_remove_same(self):
        #删除所有companyName为None的数据，去重使用
        #老去重策略弃用
        return self.get_collection().remove({"companyName": "None"})

    def find_one_and_remove(self,companyName):

        return self.get_collection().remove({"companyName": companyName})
    def remove_nophone(self,phone):
        return self.get_collection().remove({"companyTel": phone})

    def add_field_for_all(self):
        #为所有数据添加相同字段flag=1
        self.get_collection().update_many({'flag':{'$exists':False}},{'$set':{'flag':0}})

    def change_flag(self):
        #改变一个表中所有的flag为1（已推送）
        self.mong_find_many_updata({"flag":0},{"flag":1})

    def del_field(self):
        #删除flag字段用于导入接口
        self.get_collection().update({},{"$unset":{'flag':''}},False, True)

    # def get_ip(self):
    #     ip_list=list(self.get_collection().find({},no_cursor_timeout= True))
    #
    #
    #     return

if __name__ == '__main__':
    def test():
        # db = MongoDB('mongodb://rwuser:48bb67d7996f327b@10.2.1.217:57017,10.2.1.216:57017,10.2.1.218:57017/','Fangciukun','result')
        db = MongoDB('127.0.0.1:27017', 'test', 'test_coll')

        # 增加1条数据
        db.mongo_add({'name': 1})

        # 增加2条数据
        db.mongo_addmany([{'age': 2, 'score': 3}, {'score': 3}])

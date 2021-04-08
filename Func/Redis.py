from redis import ConnectionPool, Redis
from Func.conf import *


# from Singleton import *
#
# @singleton
class REDIS(object):
    def __init__(self, host, port, password, db):
        self.__host = host
        self.__port = port
        self.__password = password
        self.__db = db

        try:
            pool = ConnectionPool(host=host, port=self.__port, password=self.__password, db=self.__db,
                                  decode_responses=True)
            self.__redis = Redis(connection_pool=pool)
        except Exception as e:
            print("init error %d: %s" % (e.args[0], e.args[1]))

    def getKeys(self):
        return self.__redis.keys()

    def add(self, skey, sval):
        return self.__redis.sadd(skey, sval)

    def count(self, skey):
        count = self.__redis.scard(skey)
        return count

    def members(self, skey):
        list = self.__redis.smembers(skey)
        return list

    def ldelete(self, skey):
        return self.__redis.lpop(skey)

    def rdelete(self, skey):
        return self.__redis.rpop(skey)

    def sdelete(self, skey):
        return self.__redis.spop(skey)

    def srandom(self, skey):
        return self.__redis.srandmember(skey)

    def srem(self, skey, object):
        return self.__redis.srem(skey, object)

    def set(self, skey, sval):
        return self.__redis.set(skey, sval)

    def get(self, skey):
        return self.__redis.get(skey)

    def delete(self, skey):
        return self.__redis.delete(skey)

    def sremove(self, skey, object):
        return self.__redis.srem(skey, object)

    def expire(self, skey, ex):
        return self.__redis.expire(skey, ex)

    def sismember(self, skey, object):
        return self.__redis.sismember(skey, object)


if __name__ == "__main__":
    rds = REDIS(host=RedisHost, port=RedisPort, password=RedisPassword, db=RedisDB)
    rds.add("aa", 1)
    rds.add("aa", 2)
    rds.add("aa", 3)
    rds.add("aw", 3)
    print("count:", rds.count("aa"))
    print("count:", rds.count("aw"))
    print("member:", rds.members("aa"))
    print("member:", rds.members("aw"))
    print("delete:", rds.delete("aa"))
    print("member:", rds.members("aa"))

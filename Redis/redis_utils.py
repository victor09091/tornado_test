import redis

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'


# REDIS = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
REDIS = redis.Redis(connection_pool=pool)


def redis_str_set(key, value):
    if REDIS.set(key, value):
        REDIS.expire(key, 300)
        print "str True"
        return True
    else:
        "str False!!"
        return False

# def inspect_str_value(self, key, value):
#     res = REDIS.get(key)
#     if res:
#         return res
#     else:
#         if REDIS.set(key, value):
#             REDIS.expire(key, 300)









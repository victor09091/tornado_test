#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado

container = {}
class Session:
    def __init__(self, handler):
        self.handler = handler
        self.random_str = None

    def __genarate_random_str(self):
        import hashlib
        import time
        obj = hashlib.md5()
        # str_time = bytes(str(time.time()), encoding='utf-8')
        str_time = bytes(str(time.time()))
        obj.update(str_time)
        random_str = obj.hexdigest()
        return random_str

    # def set_value(self, key,value):
    def __setitem__(self, key, value):
        # 在container中加入随机字符串
        # 定义专属于自己的数据
        # 在客户端中写入随机字符串
        # 判断，请求的用户是否已有随机字符串
        if not self.random_str: # 重点1个: 如果我设置1成cookie的key val 这段代码一定会走,但是如果我连续对象调这个方法设置多个值,这段代码则不会走了
            random_str = self.handler.get_cookie('__session__')
            if not random_str:
                random_str = self.__genarate_random_str()
                container[random_str] = {}
            else:
                # 客户端有随机字符串
                if random_str in container.keys():
                    pass
                else:
                    random_str = self.__genarate_random_str()
                    container[random_str] = {}
            self.random_str = random_str # self.random_str = asdfasdfasdfasdf

        container[self.random_str][key] = value
        self.handler.set_cookie("__session__", self.random_str)

    def __getitem__(self, key):
        # 获取客户端的随机字符串
        # 从container中获取专属于我的数据
        #  专属信息【key】
        random_str = self.handler.get_cookie("__session__")
        print("client ", random_str)
        if not random_str:
            return None
        # 客户端有随机字符串
        user_info_dict = container.get(random_str, None)
        if not user_info_dict:
            return None
        value = user_info_dict.get(key, None)
        return value

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = Session(self)

    @property
    def nsq(self):
        return self.application.nsq

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import json
# import tornado.web
from tornado import gen
import torndb
from emial_check.process import send_email
from emial_check.assist import get_authcode, get_token

db=torndb.Connection('127.0.0.1','RUNOOB',user='root')

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


class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html' ,state = "")

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        code =self.get_argument('code')
        check_code = self.session['CheckCode']


        select_sql = 'select * from user where name=%s and password=%s'
        res = db.query(select_sql, username, password)

        if not res:
            self.render('login.html', state="用户名或密码错误！！！")
        elif code.upper() != check_code.upper():
            self.render('login.html', state="验证码错误！！！")
        else:
            self.write("登录成功")


class CheckCodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        import io
        import VerifyCode
        # 创建一个文件流
        mstream = io.BytesIO()
        # 生成图片对象和对应字符串
        img, code = VerifyCode.create_validate_code()
        img.save(mstream,"GIF")
        # 将图片信息保存到文件流

        self.session['CheckCode'] =str(code)
        # 返回图片
        self.write(mstream.getvalue())

class SendEmailHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('r.html', state="")

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        email = self.get_argument('email')
        token = get_token(username, email)
        authcode = get_authcode()
        create_sql = "insert into user_authcode (token, authcode) values ('%s', '%s')" % (token, authcode)
        db.execute(create_sql)
        res = send_email(username, authcode, email)


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('r.html' ,state = "")

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        email = self.get_argument('email')
        authcode = self.get_argument('authcode')

        select_sql = 'select * from user where name=%s'
        res = db.query(select_sql, username)
        result = ''
        token = get_token(username, email)
        authcode_sql = 'select * from user_authcode where token=%s and verification_status=0'
        authcode_res = db.query(authcode_sql, token)

        if not (username and password and email and authcode):
            result = "信息不完整,请输入完整的信息！！"
        elif res:
            result = "该用户已存在！！"
           # self.render('register_succes.html',state = "该用户已存在！")

        elif not (authcode_res and authcode_res[0]['authcode'] == authcode):
                result = "验证码错误！！"
        else:
            create_sql = "insert into user (name, password, email) values ('%s', '%s', '%s')" % (username, password, email)
            r = db.execute(create_sql)
            modify_sql = 'update user_authcode set verification_status=1 where token=%s and verification_status=0'
            db.execute(modify_sql, token)
            print r
            print "result!!!!"
            result = "注册成功！！"
        self.write(json.dumps(result))


settings = {
    'template_path':'views',
    'cookie_secret': "asdasd",
}

application = tornado.web.Application([
    (r'/login',LoginHandler),
    (r'/send_email',SendEmailHandler),
    (r'/check_code',CheckCodeHandler),
    (r'/register',RegisterHandler)
],**settings)

if __name__ == '__main__':
    # 监听端口，HTTP服务
    http_server = tornado.httpserver.HTTPServer(application)
    # 原始方式
    http_server.bind(8888)
    http_server.start(1)
    # 监听本地端口8888
    # http_server.listen(8888)
    # 启动服务
    tornado.ioloop.IOLoop.current().start()
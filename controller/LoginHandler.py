#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
from base import BaseHandler
import  json
import tornado
from tornado import gen
from db import *

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
            result = "用户名或密码错误！！！"
            # self.render('login.html', state="用户名或密码错误！！！")
        elif code.upper() != check_code.upper():
            result = "验证码错误！！！"
            # self.render('login.html', state="验证码错误！！！")
        else:
            result = "登录成功！！！"
        self.write(json.dumps(result))


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
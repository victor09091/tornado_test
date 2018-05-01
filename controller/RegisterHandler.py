#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
from base import BaseHandler
import tornado
from tornado import gen
from db import *
import json
from emial_check.send_email import send_email
from emial_check.assist import get_authcode
from Redis import REDIS, redis_str_set
# from nsq import Writer, Error


class SendEmailHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('register_test.html')

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        email = self.get_argument('email')

        model = 'email_authcode'
        token = "%s,%s,%s" % (model, username, email)

        authcode = get_authcode()
        redis_str_set(token, authcode)

        send_email(username, authcode, email)
        return self.write(json.dumps({'res_code': 200}))

    #     #nsq
    #     topic = 'log'
    #     msg = {'func': 'send_email', 'arg': [username, authcode, email]}
    #     # customize callback
    #     callback = functools.partial(self.finish_pub, topic=topic, msg=msg)
    #     self.nsq.pub(topic, msg, callback=callback)
    #
    #     self.write(msg)
    #
    # def finish_pub(self, conn, data, topic, msg):
    #     if isinstance(data, Error):
    #         # try to re-pub message again if pub failed
    #         self.nsq.pub(topic, msg)


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('register_test.html')

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        email = self.get_argument('email')
        authcode = self.get_argument('authcode')

        select_sql = 'select * from user where name=%s'
        res = db.query(select_sql, username)

        model = 'email_authcode'
        token = "%s,%s,%s" % (model, username, email)
        redis_res = REDIS.get(token)

        if not (username and password and email and authcode):
            msg = "信息不完整,请输入完整的信息！！"
        elif res:
            msg = "该用户已存在！！"

        elif not (redis_res and redis_res == authcode):
            msg = "验证码错误！！"
        else:
            msg = "注册成功！！"

            create_sql = "insert into user (name, password, email) values ('%s', '%s', '%s')" % (username, password, email)
            db.execute(create_sql)


            REDIS.delete(token)   #删除邮件验证码
            print """"""

        return self.write(json.dumps({'msg': msg, 'res_code': 200}))
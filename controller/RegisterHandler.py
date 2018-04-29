#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
from base import BaseHandler
import functools
import tornado
from tornado import gen
from db import *
import json
from emial_check.send_email import send_email
from emial_check.assist import get_authcode, get_token
from Redis import REDIS, redis_str_set
from nsq import Writer, Error

class SendEmailHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('register_test.html', state="")

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        email = self.get_argument('email')
        # token = get_token(username, email, model='email_authcode')

        token = "%s,%s,%s" % ('email_authcode', username, email)
        authcode = get_authcode()

        redis_str_set(token, authcode)

        # res = send_email(username, authcode, email)

        #nsq
        topic = 'log'
        msg = {'func': 'send_email', 'arg': [username, authcode, email]}
        # customize callback
        callback = functools.partial(self.finish_pub, topic=topic, msg=msg)
        self.nsq.pub(topic, msg, callback=callback)

        self.write(msg)

    def finish_pub(self, conn, data, topic, msg):
        if isinstance(data, Error):
            # try to re-pub message again if pub failed
            self.nsq.pub(topic, msg)


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('register_test.html' ,state = "")

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

        token = "%s,%s,%s" % ('email_authcode', username, email)
        redis_res = REDIS.get(token)

        if not (username and password and email and authcode):
            result = "信息不完整,请输入完整的信息！！"
        elif res:
            result = "该用户已存在！！"
           # self.render('register_succes.html',state = "该用户已存在！")

        elif not (redis_res and redis_res == authcode):
            result = "验证码错误！！"
        else:
            create_sql = "insert into user (name, password, email) values ('%s', '%s', '%s')" % (username, password, email)
            r = db.execute(create_sql)
            # modify_sql = 'update user_authcode set verification_status=1 where token=%s and verification_status=0'
            # db.execute(modify_sql, token)
            REDIS.delete(token)   #删除邮件验证码
            print r
            print "result!!!!"
            result = "注册成功！！"
        self.write(json.dumps(result))
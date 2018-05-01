#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import functools
import json
# from nsq import Writer, Error

from controller import LoginHandler, SendEmailHandler, CheckCodeHandler, RegisterHandler, LoginSuccessHandler

class Application(tornado.web.Application):
    def __init__(self, handlers, **settings):
        # self.nsq = Writer(['127.0.0.1:4150'])
        super(Application, self).__init__(handlers, **settings)

settings = {
    'template_path':'views',
}

application = Application([
    (r'/login',LoginHandler),
    (r'/send_email',SendEmailHandler),
    (r'/check_code',CheckCodeHandler),
    (r'/register',RegisterHandler),
    (r'/login_success', LoginSuccessHandler),
],**settings)

if __name__ == '__main__':
    # application.listen(8080)
    # tornado.ioloop.IOLoop.instance().start()
    # 监听端口，HTTP服务
    http_server = tornado.httpserver.HTTPServer(application)
    # 原始方式
    http_server.bind(8888)
    http_server.start(1)
    # 监听本地端口8888
    # http_server.listen(8888)
    # 启动服务
    tornado.ioloop.IOLoop.current().start()
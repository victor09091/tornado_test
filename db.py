#!/usr/bin/env python
# -*- coding:utf-8 -*-
import torndb

#--数据库设置
#[db]
#mysql ip
host = '127.0.0.1'
#mysql port
# port = 3306
#db name
table_db = 'RUNOOB'
table_user = 'root'
# password = root

db=torndb.Connection(host, table_db, user=table_user)

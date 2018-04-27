#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey, Float, Index, Boolean

Base = declarative_base()

class UserInfo(Base):
    __tablename__ = 'userinfo'
    # 序号nid，用户名username，密码password，邮箱email，创建时间ctime
    # 一行数据就是一个对象
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(32))
    email = Column(String(32))

class Authcode(Base):
    #邮件验证码
    __tablename__ = 'email_authcode'
    id = Column(Integer, primary_key=True)
    token = Column(VARCHAR(32))
    authcode = Column(VARCHAR(32))
    verification_status = Column(Boolean)
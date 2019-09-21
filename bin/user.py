#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's The User Model
# -- 用户模型
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/19 0:22 星期四
# ----------------------------------------------------------
from bin.app import db
from flask_login import unicode


class User(db.Model):
    """
        User 数据模型

        primary_key 如果设为True这列就是表的主键\n
        unique      如果设为True这列不允许出现重复的值\n
        index       如果设为True为这列创建索引,提升查询效率\n
        nullable    如果设为True这列允许使用空值;如果设为False这列不允许使用空值\n
        default     为这列定义默认值
    """
    # 表名
    __tablename__ = 'users'
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 昵称
    nickname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    # 密码
    password = db.Column(db.String(64), nullable=False)
    # 邮箱
    email = db.Column(db.String(64), index=True, nullable=False)
    # 性别: 0. 未知 1. 男 2. 女
    sex = db.Column(db.Integer)
    # QQ
    qq = db.Column(db.String(20))
    # 图标
    icon = db.Column(db.String(255))
    # 是否可用(默认: 1): 0. 不可用 1. 可用
    is_available = db.Column(db.Integer, nullable=False, default=1)
    # 扩展信息
    ext = db.Column(db.String(255))
    # 修改时间
    last_date = db.Column(db.DateTime, nullable=False)
    # 版本号
    version = db.Column(db.Integer, nullable=False, default=1)

    def is_authenticated(self):
        """
            is_authenticated 方法是一个误导性的名字的方法，通常这个方法应该返回True，除非对象代表一个由于某种原因没有被认证的用户。

            :return:
        """
        return True

    def is_active(self):
        """
            is_active 方法应该为用户返回True除非用户不是激活的，例如，他们已经被禁了。

            :return:
        """
        return True

    def is_anonymous(self):
        """
            is_anonymous 方法应该为那些不被获准登录的用户返回True。

            :return:
        """
        return False

    def get_id(self):
        """
            get_id 方法为用户返回唯一的unicode标识符。我们用数据库层生成唯一的id。

            :return:
        """
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

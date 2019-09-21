#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's The Role Model
# -- 角色模型
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:10 星期五
# ----------------------------------------------------------
from core.app import db
from core.models.menu import Menu


class Role(db.Model):
    """
        Role 数据模型
    """
    # 表名
    __tablename__ = "roles"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 角色编码
    role_code = db.Column(db.String(32), unique=True, nullable=False)
    # 角色名称
    role_name = db.Column(db.String(64), index=True, nullable=False)
    # 描述
    describe = db.Column(db.String(255))
    # 扩展信息
    ext = db.Column(db.String(255))
    # 修改时间
    last_date = db.Column(db.DateTime, nullable=False)
    # 版本号
    version = db.Column(db.Integer, nullable=False, default=1)

    role_menus = db.relationship("Menu", secondary="role_menus", backref="roles", lazy="dynamic", order_by=lambda: Menu.menu_code)
    role_resources = db.relationship("Resource", secondary="role_resources", backref="roles", lazy="dynamic")
    role_users = db.relationship("User", secondary="user_roles", backref="roles", lazy="dynamic")

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

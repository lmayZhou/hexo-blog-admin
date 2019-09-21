#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's The Role Menus Model
# -- 角色菜单模型
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/16 10:33 星期一
# ----------------------------------------------------------
from bin.app import db


class RoleMenus(db.Model):
    """
        RoleMenus 数据模型
    """
    # 表名
    __tablename__ = "role_menus"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 角色编码
    role_code = db.Column(db.Integer, db.ForeignKey("roles.role_code"), nullable=False)
    # 菜单编码
    menu_code = db.Column(db.String(32), db.ForeignKey("menus.menu_code"), nullable=False)
    # 修改时间
    last_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

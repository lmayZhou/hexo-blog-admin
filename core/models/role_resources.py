#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's The Role Resources Model
# -- 角色资源模型
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/16 10:34 星期一
# ----------------------------------------------------------
from core.app import db


class RoleResources(db.Model):
    """
        RoleResources 数据模型
    """
    # 表名
    __tablename__ = "role_resources"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 角色编码
    role_code = db.Column(db.String(32), db.ForeignKey("roles.role_code"), nullable=False)
    # 资源编码
    resource_code = db.Column(db.String(32), db.ForeignKey("resources.resource_code"), nullable=False)
    # 修改时间
    last_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

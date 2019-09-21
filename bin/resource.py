#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's The Resource Model
# -- 资源模型
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/16 10:24 星期一
# ----------------------------------------------------------
from bin.app import db


class Resource(db.Model):
    """
        Resource 数据模型
    """
    # 表名
    __tablename__ = "resources"
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # 上级资源编码
    parent_code = db.Column(db.String(32))
    # 资源编码
    resource_code = db.Column(db.String(32), unique=True, nullable=False)
    # 资源名称
    resource_name = db.Column(db.String(64), index=True, nullable=False)
    # 资源URL
    resource_url = db.Column(db.String(255))
    # 描述
    describe = db.Column(db.String(255))
    # 扩展信息
    ext = db.Column(db.String(255))
    # 修改时间
    last_date = db.Column(db.DateTime, nullable=False)
    # 版本号
    version = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

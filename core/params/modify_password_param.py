#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Modify Password Param
# -- 密码修改参数
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/8/10 12:20 星期五
# ----------------------------------------------------------


class ModifyPasswordParam(object):
    """
        密码修改参数
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs:  键是否存在\n
            :param kwargs: 参数
        """
        # 用户编码
        self._id = kwargs["id"] if "id" in kwargs else None
        # 原密码
        self._old_password = kwargs["old_password"] if "old_password" in kwargs else None
        # 新密码
        self._password = kwargs["password"] if "password" in kwargs else None
        # 确认密码
        self._confirm_password = kwargs["confirm_password"] if "confirm_password" in kwargs else None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def old_password(self):
        return self._old_password

    @old_password.setter
    def old_password(self, value):
        self._old_password = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def confirm_password(self):
        return self._confirm_password

    @confirm_password.setter
    def confirm_password(self, value):
        self._confirm_password = value

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

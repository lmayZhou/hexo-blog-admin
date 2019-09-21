#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Role Param
# -- 角色查询参数
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:52 星期五
# ----------------------------------------------------------
from core.params.page_param import PageParam


class RoleQueryParam(PageParam):
    """
        角色查询参数
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs: 键是否存在\n
            :param kwargs: 参数
        """
        # 初始化父类
        super().__init__(**kwargs)
        # 角色编码
        self._role_code = kwargs["role_code"] if "role_code" in kwargs else None
        # 角色名称
        self._role_name = kwargs["role_name"] if "role_name" in kwargs else None

    @property
    def role_code(self):
        return self._role_code

    @role_code.setter
    def role_code(self, value):
        self._role_code = value

    @property
    def role_name(self):
        return self._role_name

    @role_name.setter
    def role_name(self, value):
        self._role_name = value

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

    @staticmethod
    def param_dict(param):
        """
            拼装动态查询参数

            :param param:   数据
            :return:        查询条件
        """
        filters = {}
        if param.role_code:
            filters["role_code"] = param.role_code
        if param.role_name:
            filters["role_name"] = param.role_name
        return filters

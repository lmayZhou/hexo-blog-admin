#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Resource Param
# -- 资源查询参数
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:52 星期五
# ----------------------------------------------------------
from core.params.page_param import PageParam
from core.models.resource import Resource


class ResourceQueryParam(PageParam):
    """
        资源查询参数
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs: 键是否存在\n
            :param kwargs: 参数
        """
        # 初始化父类
        super().__init__(**kwargs)
        # 资源级别
        self._resource_level = kwargs["resource_level"] if "resource_level" in kwargs else None
        # 父级菜单编码
        self._parent_code = kwargs["parent_code"] if "parent_code" in kwargs else None
        # 资源编码
        self._resource_code = kwargs["resource_code"] if "resource_code" in kwargs else None
        # 资源名称
        self._resource_name = kwargs["resource_name"] if "resource_name" in kwargs else None

    @property
    def resource_level(self):
        return self._resource_level

    @resource_level.setter
    def resource_level(self, value):
        self._resource_level = value

    @property
    def parent_code(self):
        return self._parent_code

    @parent_code.setter
    def parent_code(self, value):
        self._parent_code = value

    @property
    def resource_code(self):
        return self._resource_code

    @resource_code.setter
    def resource_code(self, value):
        self._resource_code = value

    @property
    def resource_name(self):
        return self._resource_name

    @resource_name.setter
    def resource_name(self, value):
        self._resource_name = value

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

    @staticmethod
    def param_list(param):
        """
            拼装动态查询参数

            :param param:   数据
            :return:        查询条件
        """
        filters = []
        if param.parent_code:
            filters.append(Resource.parent_code == param.parent_code)
        if param.resource_code:
            filters.append(Resource.resource_code == param.resource_code)
        if param.resource_level:
            filters.append(Resource.resource_level.in_(param.resource_level))
        if param.resource_name:
            filters.append(Resource.resource_name == param.resource_name)
        return filters

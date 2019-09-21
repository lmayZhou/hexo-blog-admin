#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Menu Param
# -- 菜单查询参数
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:52 星期五
# ----------------------------------------------------------
from core.params.page_param import PageParam


class MenuQueryParam(PageParam):
    """
        菜单查询参数
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs: 键是否存在\n
            :param kwargs: 参数
        """
        # 初始化父类
        super().__init__(**kwargs)
        # 父级菜单编码
        self._parent_code = kwargs["parent_code"] if "parent_code" in kwargs else None
        # 菜单编码
        self._menu_code = kwargs["menu_code"] if "menu_code" in kwargs else None
        # 菜单名称
        self._menu_name = kwargs["menu_name"] if "menu_name" in kwargs else None

    @property
    def parent_code(self):
        return self._parent_code

    @parent_code.setter
    def parent_code(self, value):
        self._parent_code = value

    @property
    def menu_code(self):
        return self._menu_code

    @menu_code.setter
    def menu_code(self, value):
        self._menu_code = value

    @property
    def menu_name(self):
        return self._menu_name

    @menu_name.setter
    def menu_name(self, value):
        self._menu_name = value

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
        if param.parent_code:
            filters["parent_code"] = param.parent_code
        if param.menu_code:
            filters["menu_code"] = param.menu_code
        if param.menu_name:
            filters["menu_name"] = param.menu_name
        return filters

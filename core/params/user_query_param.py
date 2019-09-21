#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security User Param
# -- 用户查询参数
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:52 星期五
# ----------------------------------------------------------
from core.params.page_param import PageParam


class UserQueryParam(PageParam):
    """
        用户查询参数
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs: 键是否存在\n
            :param kwargs: 参数
        """
        # 初始化父类
        super().__init__(**kwargs)
        # 用户编码
        self._id = kwargs["id"] if "id" in kwargs else None
        # 性别
        self._sex = kwargs["sex"] if "sex" in kwargs else None
        # 用户名称
        self._nickname = kwargs["nickname"] if "nickname" in kwargs else None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        self._nickname = value

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
        if param.id:
            filters["id"] = param.id
        if param.sex:
            filters["sex"] = param.sex
        if param.nickname:
            filters["nickname"] = param.nickname
        return filters

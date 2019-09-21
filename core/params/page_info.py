#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Page Info
# -- 分页数据
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/18 17:10 星期三
# ----------------------------------------------------------


class PageInfo(object):
    """
        分页数据
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs: 键是否存在\n
            :param kwargs: 参数
        """
        # 总条数
        self._total = kwargs["total"] if "total" in kwargs.keys() else None
        # 数据
        self._rows = kwargs["rows"] if "rows" in kwargs.keys() else None

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

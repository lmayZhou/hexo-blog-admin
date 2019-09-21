#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Page Param
# -- 分页参数
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/18 14:24 星期三
# ----------------------------------------------------------


class PageParam(object):
    """
        分页参数
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs: 键是否存在\n
            :param kwargs: 参数
        """
        # 当前页码
        self._page_number = kwargs["page_number"] if "page_number" in kwargs else None
        # 每页记录数
        self._page_size = kwargs["page_size"] if "page_size" in kwargs else None
        # 排序字段
        self._sort_name = kwargs["sort_name"] if "sort_name" in kwargs else None
        # 排序方式
        self._sort_order = kwargs["sort_order"] if "sort_order" in kwargs else None

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, value):
        self._page_number = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    @property
    def sort_name(self):
        return self._sort_name

    @sort_name.setter
    def sort_name(self, value):
        self._sort_name = value

    @property
    def sort_order(self):
        return self._sort_order

    @sort_order.setter
    def sort_order(self, value):
        self._sort_order = value

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))

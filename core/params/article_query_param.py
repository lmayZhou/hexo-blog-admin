#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Article Query Param
# -- 文章查询参数
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/19 17:12 星期四
# ----------------------------------------------------------
from core.params.page_param import PageParam


class ArticleQueryParam(PageParam):
    """
        查询参数
    """
    def __init__(self, **kwargs):
        """
            实例化

            key in kwargs: 键是否存在\n
            :param kwargs: 参数
        """
        # 初始化父类
        super().__init__(**kwargs)
        # 标题
        self._title = kwargs["title"] if "title" in kwargs else None
        # 作者
        self._author = kwargs["author"] if "author" in kwargs else None
        # 分类
        self._tags = kwargs["tags"] if "tags" in kwargs else None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

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
        if param.title:
            filters["_title"] = param.title
        if param.author:
            filters["_author"] = param.author
        if param.tags:
            filters["_tags"] = param.tags
        return filters

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Article Handler
# -- 文章管理 - 业务逻辑层
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/19 17:05 星期四
# ----------------------------------------------------------
from core import LOG
from core.app import mongo_db, application
from core.constant.response_enum import ResponseEnum
from core.utils.file_utils import load_files, remove_file, write_file, read_file
from core.constant.sys_enum import SysEnum
from core.params.page_info import PageInfo
from core.models.article import Article
from core.utils import frontmatter
from core.exception.custom_errors import HandleError
from flask_pymongo import DESCENDING, ASCENDING
from core.utils.pub_utils import generate_static_website
from core.params.article_query_param import ArticleQueryParam


def load_articles(param):
    """
        加载所有文章

        :param param:   查询参数
        :return:        PageInfo
    """
    try:
        total = mongo_db.db.articles.find().count()
        if total <= 0:
            # 如果mongo中没有，就去加载目录文件
            articles = load_files(application["server"]["md_posts_path"])
            total = len(articles)
            mongo_db.db.articles.insert_many(articles)
        find_param = ArticleQueryParam.param_dict(param)
        articles = mongo_db.db.articles.find(find_param).sort(
            param.sort_name, DESCENDING if param.sort_order.upper() == "DESC" else ASCENDING).limit(
            param.page_size).skip(param.page_number * param.page_size)
        return PageInfo(total=total, rows=list(articles))
    except Exception as e:
        LOG.error("加载所有文章 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def edit_article(editor_txt, file_name):
    """
        文章编辑

        :param editor_txt:  内容
        :param file_name:   文件名
        :return:            响应结果
    """
    try:
        md_posts_path_ = application["server"]["md_posts_path"]
        write_file(file_name, ".md", editor_txt, md_posts_path_)
        post = frontmatter.loads(editor_txt).metadata
        article = Article()
        article.title = post["title"]
        article.date = post["date"]
        article.categories = post["categories"]
        article.author = post["author"]
        article.tags = post["tags"]
        if mongo_db.db.articles.find_one({"_id": file_name}):
            mongo_db.db.articles.update({"_id": file_name}, {"$set": article.__dict__})
        else:
            article.id = file_name
            article.file_name = file_name
            article.file_path = md_posts_path_ + SysEnum.SEPARATOR.value + file_name + ".md"
            mongo_db.db.articles.insert(article.__dict__)
        # 是否生成静态网页
        generate_static_website(application, LOG)
        return "SUCCESS"
    except Exception as e:
        LOG.error("文章编辑 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def delete_article(file_names):
    """
        删除文章

        :param file_names:  删除ID
        :return:            执行行数
    """
    try:
        row = 0
        if file_names:
            file_name_list = file_names.split(",")
            for item in file_name_list:
                remove_file(application["server"]["md_posts_path"] + SysEnum.SEPARATOR.value + item + ".md")
                rs = mongo_db.db.articles.remove({"_id": item})
                row += rs["n"]
        # 是否生成静态网页
        generate_static_website(application, LOG)
        return row
    except Exception as e:
        LOG.error("删除文章 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def read_article(file_name):
    """
        读取文章Md文件

        :param file_name:   文件名
        :return:            内容
    """
    try:
        return read_file(application["server"]["md_posts_path"] + SysEnum.SEPARATOR.value + file_name + ".md")
    except Exception as e:
        LOG.error("读取文章Md文件 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def modify_about_me(editor_txt):
    """
        修改关于我Md信息

        :param editor_txt: 内容
    """
    try:
        write_file("index", ".md", editor_txt, application["server"]["md_about_path"])
        # 是否生成静态网页
        generate_static_website(application, LOG)
        return "SUCCESS"
    except Exception as e:
        LOG.error("修改关于我Md信息 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def read_about_me():
    """
        读取关于我Md文件

        :return: 内容
    """
    try:
        return read_file(application["server"]["md_about_path"] + SysEnum.SEPARATOR.value + "index.md")
    except Exception as e:
        LOG.error("读取关于我Md文件 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)

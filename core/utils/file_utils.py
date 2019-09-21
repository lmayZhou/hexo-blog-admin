#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's File Utils
# -- 文件处理工具集
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# @email lmay@lmaye.com
# Date: 2018年4月11日 00:31:23
# ----------------------------------------------------------
import os
from time import strftime, localtime
from core import LOG
from core.constant.sys_enum import SysEnum
from core.utils import frontmatter
from core.models.article import Article


def remove_file(file_path):
    """
        文件删除

        :param file_path: 文件路径
    """
    os.remove(file_path)


def read_file(file_path):
    try:
        if not file_path:
            LOG.error("File Path is None.")
            return None
        f = open(file_path, "r", encoding='UTF-8', newline="\n")
        return f.read()
    except Exception as e:
        raise e


def write_file(file_name, file_suffix, content, output_path):
    """
        文件生成

        :param str file_name:   文件名
        :param str file_suffix: 文件后缀
        :param str content:     写入内容
        :param str output_path: 输出路径
        :return:                None
    """
    try:
        if not file_name:
            LOG.error("File name is None.")
            return None
        if not file_suffix:
            LOG.error("File suffix is None.")
            return None
        if not output_path:
            LOG.error("Output path is None.")
            return None
        # 目录是否存在
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        """
            1、\n 软回车：
            在Windows 中表示换行且回到下一行的最开始位置。相当于Mac OS 里的 \r 的效果。
            在Linux、unix 中只表示换行，但不会回到下一行的开始位置。
            
            2、\r 软空格：
            在Linux、unix 中表示返回到当行的最开始位置。
            在Mac OS 中表示换行且返回到下一行的最开始位置，相当于Windows 里的 \n 的效果。
            
            'U' mode is deprecated and will raise an exception in future versions of Python.
            It has no effect in Python 3. Use newline to control universal newlines mode.
            ※ Python3 newline="\n" [指定换行符]
        """
        f = open(output_path + SysEnum.SEPARATOR.value + file_name + file_suffix, 'w+', encoding='UTF-8', newline="\n")
        # LOG.info("写入内容：{}".format(content))
        f.write(content)
        f.close()
        LOG.info("文件写入成功: {}".format(output_path + SysEnum.SEPARATOR.value + file_name + file_suffix))
    except Exception as e:
        raise e


def load_files(load_path):
    """
        加载文件列表

        :param load_path:
        :return:
    """
    if not load_path:
        LOG.error("Load path is None.")
        return None
    items = os.listdir(load_path)
    items.sort(key=lambda x: compare(load_path, x), reverse=True)
    result = []
    for item in items:
        file_path = load_path + SysEnum.SEPARATOR.value + item
        post = frontmatter.load(file_path)
        article = Article()
        _file_name = str(item).replace(".md", "")
        article.id = _file_name
        article.file_name = _file_name
        article.title = post["title"]
        article.date = post["date"]
        article.categories = post["categories"]
        article.author = post["author"]
        article.tags = post["tags"]
        article.file_path = file_path
        result.append(article.__dict__)
    return result


def compare(load_path, file):
    """
        文件修改时间

        :param load_path:
        :param file:
        :return:
    """
    stat_file = os.stat(load_path + SysEnum.SEPARATOR.value + file)
    last_modify_time = stat_file.st_mtime
    LOG.info(strftime('%Y/%m/%d %H:%M:%S', localtime(last_modify_time)))
    return last_modify_time

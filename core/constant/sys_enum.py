#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's System Enum
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月13日 15:44:23
# ----------------------------------------------------------
import os
from enum import Enum, unique


@unique
class SysEnum(Enum):
    """
        System Enum
    """
    # 系统目录分隔符
    SEPARATOR = os.path.sep
    # 当前目录
    CURRENT_PATH = os.path.abspath(".")
    # 资源目录
    RESOURCES_PATH = CURRENT_PATH + SEPARATOR + "resources"
    # Logging配置文件
    LOGGING_PATH = RESOURCES_PATH + SEPARATOR + "logging.conf"
    # YML配置文件
    DB_PATH = RESOURCES_PATH + SEPARATOR + "databases.yml"
    # JSON配置文件
    JSON_PATH = RESOURCES_PATH + SEPARATOR + "test.json"
    # 系统应用配置文件
    APPLICATION_PATH = RESOURCES_PATH + SEPARATOR + "application.yml"
    # Temp目录
    TEMP_PATH = os.path.join(RESOURCES_PATH + SEPARATOR, "temp")
    # 分页显示
    POSTS_PER_PAGE = 3
    # 全文搜索目录
    WHOOSH_BASE = os.path.join(RESOURCES_PATH + SEPARATOR, "search_db")
    # 搜索结果返回的最大数量
    MAX_SEARCH_RESULTS = 50

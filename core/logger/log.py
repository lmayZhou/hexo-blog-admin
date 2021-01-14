#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Get Logger
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月1日 16:20:04
# ----------------------------------------------------------
import logging.config
from core.constant.sys_enum import SysEnum


def logger():
    logging.config.fileConfig(SysEnum.LOGGING_PATH.value)
    return logging.getLogger("hexo-blog-admin")

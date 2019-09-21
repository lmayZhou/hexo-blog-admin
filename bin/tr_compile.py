#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 编译成二进制的 *.mo 资源文件
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# @email lmay@lmaye.com
# Date: 2018年4月4日 00:41:55
# ----------------------------------------------------------

import os

os.system('pybabel compile -d ../resources/translations')

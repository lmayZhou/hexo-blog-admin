#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 国际化和本地化脚本 [更新]
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# @email lmay@lmaye.com
# Date: 2018年4月4日 00:40:59
# ----------------------------------------------------------

import os

os.system('pybabel extract -F ../resources/babel.cfg -k lazy_gettext -o ../resources/messages.pot ..')
os.system('pybabel update -i ../resources/messages.pot -d ../resources/translations')
# 删除的文件
os.unlink('../resources/messages.pot')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 国际化和本地化脚本 [生成]
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# @email lmay@lmaye.com
# Date: 2018年4月4日 00:40:55
# ----------------------------------------------------------

import os

os.system('pybabel extract -F ../resources/babel.cfg -k lazy_gettext -o ../resources/messages.pot ..')
os.system('pybabel init -i ../resources/messages.pot -d ../resources/translations -l zh')
# 删除的文件
os.unlink('../resources/messages.pot')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Decorators
# -- 装饰器
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年3月2日 12:51:10
# ----------------------------------------------------------
import time
from threading import Thread


def i_async(f):
    """
        异步装饰器

        :param f:
        :return:
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def timmer(func):
    """
        统计运行时间

        :param func:
        :return:
    """
    def warpper(*args, **kwargs):
        strat_time = time.time()
        func()
        stop_time = time.time()
        print("the func run time is %s" % (stop_time - strat_time))
    return warpper

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- CustomJSONEncoder
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# @email lmay@lmaye.com
# Date: 2018年4月4日 00:16:43
# ----------------------------------------------------------
import random
import string
import subprocess
from flask.json import JSONEncoder
from flask_login import unicode


class CustomJSONEncoder(JSONEncoder):
    """
        This class adds support for lazy translation texts to Flask's
        JSON encoder. This is necessary when flashing translated texts.
    """
    def default(self, obj):
        from speaklater import is_lazy_string
        if is_lazy_string(obj):
            try:
                return unicode(obj)  # python 2
            except NameError:
                return str(obj)  # python 3
        return super(CustomJSONEncoder, self).default(obj)


def generate_random_str(length=8):
    """
        生成一个指定长度的随机字符串
        string.digits = 0123456789
        string.ascii_letters = abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ

        :param length:  长度
        :return:        生成字符串
    """
    return ''.join([random.choice(string.digits + string.ascii_letters) for i in range(length)])


def generate_static_website(application, log):
    """
        生成静态网页
        -- shell 脚本

        :param application: 应用配置
        :param log:         日志
        :return:
    """
    try:
        if application["server"]["is_generate"]:
            cmd = ["/bin/bash", application["server"]["shell_script_path"]]
            r = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = r.communicate()
            log.info("静态网页生成脚本执行结果: [{}] {}".format(out, err))
    except Exception as e:
        log.error("静态网页生成脚本执行失败: {}".format(e))

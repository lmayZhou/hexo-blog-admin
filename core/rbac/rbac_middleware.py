#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's RBAC Middleware
# -- rbac 中间件
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/17 11:35 星期二
# ----------------------------------------------------------
from core.utils import read_config
from core.constant.sys_enum import SysEnum
from flask import redirect, session, request, url_for, abort
import re


class RBACMiddleware(object):
    @staticmethod
    def rbac_middleware():
        application = read_config.read_yml(SysEnum.APPLICATION_PATH.value)
        rbac_whitelist = application["rbac"]["whitelist"]
        # 当前请求url
        url_rule = str(request.path)
        # 过滤白名单，支持正则
        for url in rbac_whitelist["PASS_URL_LIST"]:
            if re.match(url, url_rule):
                return None
        # 获取权限
        permission_url_list = session.get("SESSION_PERMISSION_URL")
        # 获取用户对象
        user = session.get("user_id")
        # 如果其中一个没有获取到，需要重新登陆
        if not permission_url_list or not user:
            return redirect(url_for("login"))
        # TODO:处理: 如果当前请求路径不存数据库
        # if url_rule not in permission_url_list:
        #     return abort(404)

        # 定义一个标识
        flag = False
        for db_url in permission_url_list:
            # pattern = ^db_url$,开头和结束，精确匹配，当然，权限数据表中可以使用正则，这里支持正则
            pattern = rbac_whitelist["URL_REGEX"].format(db_url)
            if re.match(pattern, url_rule):
                # 匹配到之后，表示改为True，跳出循环
                flag = True
                break

        # 如果没有权限，则会返回定义的页面
        if not flag:
            return abort(403)

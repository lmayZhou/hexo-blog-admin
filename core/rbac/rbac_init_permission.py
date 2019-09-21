#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's RBAC Init Permission
# -- 权限初始化
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/16 16:50 星期一
# ----------------------------------------------------------
from core.models.role import Role
from flask import session


class RBACInitPermission(object):
    """
        RBAC 权限初始化
    """
    def __init__(self, user):
        """
            获取当前用户权限，并写入session

            :param user:    用户
        """
        # 当前用户资源
        permission_url_list = [row.resource_url for row in user.user_resources.all()]

        # 当前用户菜单
        permission_menu_list = [
            {
                "menu_code": row.menu_code,
                "menu_name": row.menu_name,
                "parent_code": row.parent_code,
                "menu_url": row.menu_url
             } for row in user.user_menus.all() if row.menu_code
        ]

        # 当前用户角色
        for it in user.user_roles.all():
            record = Role.query.filter_by(role_code=it.role_code).first()
            # 角色资源
            permission_url_list += [row.resource_url for row in record.role_resources.all()]
            # 角色菜单
            permission_menu_list += [
                {
                    "menu_code": row.menu_code,
                    "menu_name": row.menu_name,
                    "parent_code": row.parent_code,
                    "menu_url": row.menu_url
                } for row in record.role_menus.all() if row.menu_code
            ]
        # 写入到session
        session["SESSION_PERMISSION_URL"] = permission_url_list
        session["SESSION_PERMISSION_MENU"] = permission_menu_list

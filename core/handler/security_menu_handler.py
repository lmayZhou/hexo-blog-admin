#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Menu Handler
# -- 菜单权限管理 - 业务逻辑层
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:35 星期五
# ----------------------------------------------------------
import datetime
from core.models.user import User
from core.models.role import Role
from core.app import db
from core import LOG
from core.constant.response_enum import ResponseEnum
from core.exception.custom_errors import HandleError
from core.params.page_info import PageInfo
from core.models.menu import Menu
from core.params.menu_query_param import MenuQueryParam
from core.models.role_menus import RoleMenus
from core.models.user_menus import UserMenus


def menu_page(param):
    """
        菜单列表加载

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = MenuQueryParam.param_dict(param)
        menus = Menu.query.filter_by(**filters).order_by(param.sort_name + " " + param.sort_order) \
            .paginate(param.page_number, param.page_size, False)
        rows = []
        for it in menus.items:
            it = it.__dict__
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            rows.append(it)
        return PageInfo(total=menus.total, rows=rows)
    except Exception as e:
        LOG.error("菜单表加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_list(param):
    """
        菜单 - List

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = MenuQueryParam.param_dict(param)
        menus = Menu.query.filter_by(**filters).order_by(Menu.id.asc()).all()
        rows = []
        for it in menus:
            it = it.__dict__
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            # JS 前端处理
            # if "last_date" in it:
            #     it["last_date"] = it["last_date"].strftime("%Y-%m-%d %H:%M:%S")
            rows.append(it)
        return rows
    except Exception as e:
        LOG.error("菜单List加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_delete(ids):
    """
        菜单删除

        :param ids: 删除ID
        :return:    响应结果
    """
    try:
        row = 0
        if ids:
            file_name_list = ids.split(",")
            for item in file_name_list:
                rs = Menu.query.filter(Menu.id == item).first()
                if rs:
                    is_exist_children = Menu.query.filter(Menu.parent_code == rs.menu_code).all()
                    if len(is_exist_children) > 0:
                        raise HandleError(ResponseEnum.FAILURE.value, "当前菜单[{}]存在子级菜单，请先删除所有子级菜单！"
                                          .format(rs.menu_code))
                    # 删除关联的表
                    RoleMenus.query.filter(RoleMenus.menu_code == rs.menu_code).delete()
                    UserMenus.query.filter(UserMenus.menu_code == rs.menu_code).delete()
                    db.session.delete(rs)
                    db.session.commit()
                    row += 1
        return row
    except HandleError as e:
        LOG.error("删除菜单 - 异常：{}".format(e))
        raise e
    except Exception as e:
        LOG.error("删除菜单 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_details(id):
    """
        菜单详情

        :param id:  主键
        :return:    响应结果
    """
    try:
        return Menu.query.filter(Menu.id == id).first()
    except Exception as e:
        LOG.error("查看菜单详情 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_add(menu):
    """
        菜单新增

        :param menu:    数据
        :return:        响应结果
    """
    try:
        menu.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        menu.version = 1
        db.session.add(menu)
        db.session.commit()
        return menu
    except Exception as e:
        LOG.error("菜单新增 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_edit(menu):
    """
        菜单编辑

        :param menu:    数据
        :return:        响应结果
    """
    try:
        # 根据ID查询
        original_menu = Menu.query.filter(Menu.id == menu.id).first()
        original_menu.parent_code = menu.parent_code
        original_menu.menu_code = menu.menu_code
        original_menu.menu_name = menu.menu_name
        original_menu.menu_url = menu.menu_url
        original_menu.describe = menu.describe
        original_menu.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        original_menu.version += 1
        db.session.commit()
        return original_menu
    except Exception as e:
        LOG.error("菜单编辑 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_roles_data(menu_code):
    """
        菜单角色数据加载

        :param menu_code:   参数
        :return:            menu_name, roles, menu_roles
    """
    try:
        # 1. 查出所有的角色
        roles = Role.query.all()
        # 2. 查出拥有当前菜单权限的所有菜单角色
        menu = Menu.query.filter(Menu.menu_code == menu_code).first()
        menu_roles = []
        for it in menu.menu_roles.all():
            menu_roles.append({"role_code": it.role_code})
        return menu.menu_name, roles, menu_roles
    except Exception as e:
        LOG.error("菜单角色数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_users_data(menu_code):
    """
        菜单用户数据加载

        :param menu_code:   参数
        :return:            menu_name, users, menu_users
    """
    try:
        # 1. 查出所有的用户
        users = User.query.all()
        # 2. 查出拥有当前菜单权限的所有菜单用户
        menu = Menu.query.filter(Menu.menu_code == menu_code).first()
        menu_users = []
        for it in menu.menu_users.all():
            menu_users.append({"user_id": it.id})
        return menu.menu_name, users, menu_users
    except Exception as e:
        LOG.error("菜单用户数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_roles_save(menu_code, role_codes):
    """
        菜单角色保存

        :param menu_code:   菜单编号
        :param role_codes:  角色编号List
        :return:            SUCCESS
    """
    try:
        RoleMenus.query.filter(RoleMenus.menu_code == menu_code).delete()
        role_menus = []
        for role_code in role_codes:
            role_menu = RoleMenus(menu_code=menu_code, role_code=role_code,
                                  last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            role_menus.append(role_menu)
        if role_menus:
            db.session.add_all(role_menus)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("菜单角色保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def menu_users_save(menu_code, user_ids):
    """
        菜单用户保存

        :param menu_code:   菜单编号
        :param user_ids:    用户ID List
        :return:            SUCCESS
    """
    try:
        UserMenus.query.filter(UserMenus.menu_code == menu_code).delete()
        user_menus = []
        for user_id in user_ids:
            user_menu = UserMenus(menu_code=menu_code, user_id=user_id,
                                  last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            user_menus.append(user_menu)
        if user_menus:
            db.session.add_all(user_menus)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("菜单用户保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Role Handler
# -- 角色权限管理 - 业务逻辑层
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:35 星期五
# ----------------------------------------------------------
import datetime
from core.models.user import User
from core.app import db
from core import LOG
from core.constant.response_enum import ResponseEnum
from core.exception.custom_errors import HandleError
from core.params.page_info import PageInfo
from core.models.role import Role
from core.params.role_query_param import RoleQueryParam
from core.models.role_menus import RoleMenus
from core.models.role_resources import RoleResources
from core.models.user_roles import UserRoles
from core.models.resource import Resource
from core.models.menu import Menu


def role_page(param):
    """
        角色列表加载

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = RoleQueryParam.param_dict(param)
        roles = Role.query.filter_by(**filters).order_by(param.sort_name + " " + param.sort_order) \
            .paginate(param.page_number, param.page_size, False)
        rows = []
        for it in roles.items:
            it = it.__dict__
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            rows.append(it)
        return PageInfo(total=roles.total, rows=rows)
    except Exception as e:
        LOG.error("角色表加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_list(param):
    """
        角色 - List

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = RoleQueryParam.param_dict(param)
        roles = Role.query.filter_by(**filters).order_by(Role.id.asc()).all()
        rows = []
        for it in roles:
            it = it.__dict__
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            # JS 前端处理
            # if "last_date" in it:
            #     it["last_date"] = it["last_date"].strftime("%Y-%m-%d %H:%M:%S")
            rows.append(it)
        return rows
    except Exception as e:
        LOG.error("角色List加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_delete(ids):
    """
        角色删除

        :param ids: 删除ID
        :return:    响应结果
    """
    try:
        row = 0
        if ids:
            file_name_list = ids.split(",")
            for item in file_name_list:
                rs = Role.query.filter(Role.id == item).first()
                if rs:
                    # 删除关联的表
                    RoleResources.query.filter(RoleResources.role_code == rs.role_code).delete()
                    RoleMenus.query.filter(RoleMenus.role_code == rs.role_code).delete()
                    UserRoles.query.filter(UserRoles.role_code == rs.role_code).delete()
                    db.session.delete(rs)
                    db.session.commit()
                    row += 1
        return row
    except Exception as e:
        LOG.error("删除角色 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_details(id):
    """
        角色详情

        :param id:  主键
        :return:    响应结果
    """
    try:
        return Role.query.filter(Role.id == id).first()
    except Exception as e:
        LOG.error("查看角色详情 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_add(role):
    """
        角色新增

        :param role:    数据
        :return:        响应结果
    """
    try:
        role.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        role.version = 1
        db.session.add(role)
        db.session.commit()
        return role
    except Exception as e:
        LOG.error("角色新增 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_edit(role):
    """
        角色编辑

        :param role:    数据
        :return:        响应结果
    """
    try:
        # 根据ID查询
        original_role = Role.query.filter(Role.id == role.id).first()
        original_role.role_code = role.role_code
        original_role.role_name = role.role_name
        original_role.describe = role.describe
        original_role.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        original_role.version += 1
        db.session.commit()
        return original_role
    except Exception as e:
        LOG.error("角色编辑 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_menus_data(role_code):
    """
        角色菜单数据加载

        :param role_code:   参数
        :return:            role_name, z_nodes
    """
    try:
        z_nodes = []
        # 1. 查出所有的菜单
        menus = Menu.query.all()
        # 2. 查出拥有当前角色权限的所有角色菜单
        role = Role.query.filter(Role.role_code == role_code).first()
        role_menus = []
        for it in role.role_menus.all():
            role_menus.append(it.menu_code)
        for menu in menus:
            parent_code = menu.parent_code
            menu_code = menu.menu_code
            dt = {"id": menu_code, "pId": parent_code, "name": menu.menu_name + " [" + menu_code + "]"}
            if parent_code:
                dt["open"] = True
            if menu_code in role_menus:
                dt["checked"] = True
            z_nodes.append(dt)
        return role.role_name, z_nodes
    except Exception as e:
        LOG.error("角色菜单数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_resources_data(role_code):
    """
        角色资源数据加载

        :param role_code:   参数
        :return:            role_name, z_nodes
    """
    try:
        z_nodes = []
        # 1. 查出所有的资源
        resources = Resource.query.all()
        # 2. 查出拥有当前角色权限的所有角色资源
        role = Role.query.filter(Role.role_code == role_code).first()
        role_resources = []
        for it in role.role_resources.all():
            role_resources.append(it.resource_code)
        for resource in resources:
            parent_code = resource.parent_code
            resource_code = resource.resource_code
            dt = {"id": resource_code, "pId": parent_code, "name": resource.resource_name + " [" + resource_code + "]"}
            if parent_code:
                dt["open"] = True
            if resource_code in role_resources:
                dt["checked"] = True
            z_nodes.append(dt)
        return role.role_name, z_nodes
    except Exception as e:
        LOG.error("角色资源数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_users_data(role_code):
    """
        角色用户数据加载

        :param role_code:   参数
        :return:            role_name, users, role_users
    """
    try:
        # 1. 查出所有的用户
        users = User.query.all()
        # 2. 查出拥有当前角色权限的所有角色用户
        role = Role.query.filter(Role.role_code == role_code).first()
        role_users = []
        for it in role.role_users.all():
            role_users.append({"user_id": it.id})
        return role.role_name, users, role_users
    except Exception as e:
        LOG.error("角色用户数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_menus_save(role_code, menu_codes):
    """
        角色菜单保存

        :param role_code:   角色编号
        :param menu_codes:  菜单编号List
        :return:            SUCCESS
    """
    try:
        RoleMenus.query.filter(RoleMenus.role_code == role_code).delete()
        role_menus = []
        for menu_code in menu_codes:
            role_menu = RoleMenus(role_code=role_code, menu_code=menu_code,
                                  last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            role_menus.append(role_menu)
        if role_menus:
            db.session.add_all(role_menus)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("角色菜单保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_resources_save(role_code, resource_codes):
    """
        角色资源保存

        :param role_code:       角色编号
        :param resource_codes:  资源编号List
        :return:                SUCCESS
    """
    try:
        RoleResources.query.filter(RoleResources.role_code == role_code).delete()
        role_resources = []
        for resource_code in resource_codes:
            role_resource = RoleResources(role_code=role_code, resource_code=resource_code,
                                          last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            role_resources.append(role_resource)
        if role_resources:
            db.session.add_all(role_resources)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("角色资源保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def role_users_save(role_code, user_ids):
    """
        角色用户保存

        :param role_code:   角色编号
        :param user_ids:    用户ID List
        :return:            SUCCESS
    """
    try:
        UserRoles.query.filter(UserRoles.role_code == role_code).delete()
        user_roles = []
        for user_id in user_ids:
            user_role = UserRoles(role_code=role_code, user_id=user_id,
                                  last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            user_roles.append(user_role)
        if user_roles:
            db.session.add_all(user_roles)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("角色用户保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)

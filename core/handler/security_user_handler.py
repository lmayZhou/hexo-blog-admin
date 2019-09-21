#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security User Handler
# -- 用户权限管理 - 业务逻辑层
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:35 星期五
# ----------------------------------------------------------
import datetime
from core.utils.emails import user_add_notification
from core.utils.security import Security
from core.models.role import Role
from core.app import db, application
from core import LOG
from core.constant.response_enum import ResponseEnum
from core.exception.custom_errors import HandleError, VerifyError
from core.params.page_info import PageInfo
from core.models.user import User
from core.params.user_query_param import UserQueryParam
from core.models.user_menus import UserMenus
from core.models.user_roles import UserRoles
from core.models.user_resources import UserResources
from core.models.menu import Menu
from core.models.resource import Resource
from core.utils.pub_utils import generate_random_str


def user_page(param):
    """
        用户列表加载

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = UserQueryParam.param_dict(param)
        users = User.query.filter_by(**filters).order_by(param.sort_name + " " + param.sort_order) \
            .paginate(param.page_number, param.page_size, False)
        rows = []
        for it in users.items:
            it = it.__dict__
            # 删除密码
            del it["password"]
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            rows.append(it)
        return PageInfo(total=users.total, rows=rows)
    except Exception as e:
        LOG.error("用户表加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_list(param):
    """
        用户 - List

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = UserQueryParam.param_dict(param)
        users = User.query.filter_by(**filters).order_by(User.id.asc()).all()
        rows = []
        for it in users:
            it = it.__dict__
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            # JS 前端处理
            # if "last_date" in it:
            #     it["last_date"] = it["last_date"].strftime("%Y-%m-%d %H:%M:%S")
            rows.append(it)
        return rows
    except Exception as e:
        LOG.error("用户List加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_delete(ids):
    """
        用户删除

        :param ids: 删除ID
        :return:    响应结果
    """
    try:
        row = 0
        if ids:
            file_name_list = ids.split(",")
            for item in file_name_list:
                rs = User.query.filter(User.id == item).first()
                if rs:
                    # 删除关联的表
                    UserMenus.query.filter(UserMenus.user_id == rs.id).delete()
                    UserResources.query.filter(UserResources.user_id == rs.id).delete()
                    UserRoles.query.filter(UserRoles.user_id == rs.id).delete()
                    db.session.delete(rs)
                    db.session.commit()
                    row += 1
        return row
    except Exception as e:
        LOG.error("删除用户 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_is_disable(user_id, is_available):
    """
        是否禁用

        :param user_id:         用户ID
        :param is_available:    禁用状态
        :return:                响应结果
    """
    try:
        # 根据ID查询
        original_user = User.query.filter(User.id == user_id).first()
        original_user.id = user_id
        original_user.is_available = is_available
        original_user.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        original_user.version += 1
        db.session.commit()
        original_user.password = None
        return original_user
    except Exception as e:
        LOG.error("是否禁用处理 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_details(id):
    """
        用户详情

        :param id:  主键
        :return:    响应结果
    """
    try:
        user = User.query.filter(User.id == id).first()
        user.password = None
        return user
    except Exception as e:
        LOG.error("查看用户详情 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_add(user):
    """
        用户新增

        :param user:    数据
        :return:        响应结果
    """
    try:
        rs = User.query.filter(User.nickname == user.nickname).first()
        if rs:
            raise VerifyError(ResponseEnum.PARAM_VALIDATE_ERROR.value,
                              {"nickname": "[{}] 该昵称已被注册！".format(user.nickname)})
        rs = User.query.filter(User.email == user.email).first()
        if rs:
            raise VerifyError(ResponseEnum.PARAM_VALIDATE_ERROR.value,
                              {"email": "[{}] 该邮箱已被注册！".format(user.email)})
        sc = Security(application["server"]["PRIVATE_KEY"])
        random_password = generate_random_str(8)
        # 发送邮件
        user_add_notification(user, random_password)
        user.password = sc.encrypt(random_password).replace("\n", "")
        user.is_available = 1
        user.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        user.version = 1
        db.session.add(user)
        db.session.commit()
        user.password = None
        return user
    except VerifyError as e:
        LOG.error("参数校验 - 异常：{}".format(e))
        raise e
    except Exception as e:
        LOG.error("用户新增 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_edit(user):
    """
        用户编辑

        :param user:    数据
        :return:        响应结果
    """
    try:
        # 根据ID查询
        original_user = User.query.filter(User.id == user.id).first()
        if not original_user:
            raise HandleError(ResponseEnum.FAILURE.value, "[{}] 该用户不存在！".format(user.id))
        rs = User.query.filter(User.email == user.email).first()
        # 编辑的名称是否被占用
        if rs and original_user.email != user.email:
            raise VerifyError(ResponseEnum.PARAM_VALIDATE_ERROR.value,
                              {"email": "[{}] 该邮箱已被注册！".format(user.email)})
        original_user.id = user.id
        original_user.email = user.email
        original_user.sex = user.sex
        original_user.qq = user.qq
        original_user.icon = user.icon
        original_user.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        original_user.version += 1
        db.session.commit()
        original_user.password = None
        return original_user
    except VerifyError as e:
        LOG.error("参数校验 - 异常：{}".format(e))
        raise e
    except HandleError as e:
        LOG.error("用户编辑 - 异常：{}".format(e))
        raise e
    except Exception as e:
        LOG.error("用户编辑 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def modify_password(param):
    """
        密码修改

        :param param:    用户参数
        :return:        响应数据
    """
    try:
        # 根据ID查询
        x = "lmay0421        "
        original_user = User.query.filter(User.id == param.id).first()
        if not original_user:
            raise HandleError(ResponseEnum.FAILURE.value, "该用户不存在！")
        sc = Security(application["server"]["PRIVATE_KEY"])
        if original_user.password != sc.encrypt(param.old_password).replace("\n", ""):
            raise VerifyError(ResponseEnum.PARAM_VALIDATE_ERROR.value, {"old_password": "旧的密码错误！"})
        original_user.password = sc.encrypt(param.password).replace("\n", "")
        original_user.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        original_user.version += 1
        db.session.commit()
        original_user.password = None
        return original_user
    except VerifyError as e:
        LOG.error("参数校验 - 异常：{}".format(e))
        raise e
    except HandleError as e:
        LOG.error("密码修改 - 异常：{}".format(e))
        raise e
    except Exception as e:
        LOG.error("密码修改 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_menus_data(user_id):
    """
        用户菜单数据加载

        :param user_id: 参数
        :return:        user.nickname, z_nodes
    """
    try:
        z_nodes = []
        # 1. 查出所有的菜单
        menus = Menu.query.all()
        # 2. 查出拥有当前用户权限的所有用户菜单
        user = User.query.filter(User.id == user_id).first()
        user_menus = []
        for it in user.user_menus.all():
            user_menus.append(it.menu_code)
        for menu in menus:
            parent_code = menu.parent_code
            menu_code = menu.menu_code
            dt = {"id": menu_code, "pId": parent_code, "name": menu.menu_name + " [" + menu_code + "]"}
            if parent_code:
                dt["open"] = True
            if menu_code in user_menus:
                dt["checked"] = True
            z_nodes.append(dt)
        return user.nickname, z_nodes
    except Exception as e:
        LOG.error("用户菜单数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_resources_data(user_id):
    """
        用户资源数据加载

        :param user_id: 参数
        :return:        user.nickname, z_nodes
    """
    try:
        z_nodes = []
        # 1. 查出所有的资源
        resources = Resource.query.all()
        # 2. 查出拥有当前用户权限的所有用户资源
        user = User.query.filter(User.id == user_id).first()
        user_resources = []
        for it in user.user_resources.all():
            user_resources.append(it.resource_code)
        for resource in resources:
            parent_code = resource.parent_code
            resource_code = resource.resource_code
            dt = {"id": resource_code, "pId": parent_code, "name": resource.resource_name + " [" + resource_code + "]"}
            if parent_code:
                dt["open"] = True
            if resource_code in user_resources:
                dt["checked"] = True
            z_nodes.append(dt)
        return user.nickname, z_nodes
    except Exception as e:
        LOG.error("用户资源数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_roles_data(user_id):
    """
        用户角色数据加载

        :param user_id: 参数
        :return:        user.nickname, roles, user_roles
    """
    try:
        # 1. 查出所有的角色
        roles = Role.query.all()
        # 2. 查出拥有当前用户权限的所有用户角色
        user = User.query.filter(User.id == user_id).first()
        user_roles = []
        for it in user.user_roles.all():
            user_roles.append({"role_code": it.role_code})
        return user.nickname, roles, user_roles
    except Exception as e:
        LOG.error("用户角色数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_menus_save(user_id, menu_codes):
    """
        用户菜单保存

        :param user_id:     用户编号
        :param menu_codes:  菜单编号List
        :return:            SUCCESS
    """
    try:
        UserMenus.query.filter(UserMenus.user_id == user_id).delete()
        user_menus = []
        for menu_code in menu_codes:
            user_menu = UserMenus(user_id=user_id, menu_code=menu_code,
                                  last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            user_menus.append(user_menu)
        if user_menus:
            db.session.add_all(user_menus)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("用户菜单保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_resources_save(user_id, resource_codes):
    """
        用户资源保存

        :param user_id:         用户编号
        :param resource_codes:  资源编号List
        :return:                SUCCESS
    """
    try:
        UserResources.query.filter(UserResources.user_id == user_id).delete()
        user_resources = []
        for resource_code in resource_codes:
            user_role = UserResources(user_id=user_id, resource_code=resource_code,
                                      last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            user_resources.append(user_role)
        if user_resources:
            db.session.add_all(user_resources)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("用户资源保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def user_roles_save(user_id, role_codes):
    """
        用户角色保存

        :param user_id:     用户编号
        :param role_codes:  角色编号List
        :return:            SUCCESS
    """
    try:
        UserRoles.query.filter(UserRoles.user_id == user_id).delete()
        user_roles = []
        for role_code in role_codes:
            user_role = UserRoles(user_id=user_id, role_code=role_code,
                                  last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            user_roles.append(user_role)
        if user_roles:
            db.session.add_all(user_roles)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("用户角色保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)

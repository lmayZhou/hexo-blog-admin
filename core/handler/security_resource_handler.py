#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Resource Resource Handler
# -- 资源权限管理 - 业务逻辑层
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/20 17:35 星期五
# ----------------------------------------------------------
import datetime
from sqlalchemy import text
from core.models.user import User
from core.models.role import Role
from core.app import db
from core import LOG
from core.constant.response_enum import ResponseEnum
from core.exception.custom_errors import HandleError
from core.params.page_info import PageInfo
from core.models.resource import Resource
from core.params.resource_query_param import ResourceQueryParam
from core.models.role_resources import RoleResources
from core.models.user_resources import UserResources


def resource_page(param):
    """
        资源列表加载

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = ResourceQueryParam.param_list(param)
        resources = Resource.query.filter(*filters).order_by(text(param.sort_name + " " + param.sort_order)) \
            .paginate(param.page_number, param.page_size, False)
        rows = []
        for it in resources.items:
            it = it.__dict__
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            rows.append(it)
        return PageInfo(total=resources.total, rows=rows)
    except Exception as e:
        LOG.error("资源表加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_list(param):
    """
        资源 - List

        filter_by用于查询简单的列名，不支持比较运算符;
        filter比filter_by的功能更强大，支持比较运算符，支持or_、in_等语法;

        :param param:   查询参数
        :return:        响应结果
    """
    try:
        filters = ResourceQueryParam.param_list(param)
        resources = Resource.query.filter(*filters).order_by(Resource.resource_code.asc()).all()
        rows = []
        for it in resources:
            it = it.__dict__
            if "_sa_instance_state" in it:
                del it["_sa_instance_state"]
            # JS 前端处理
            # if "last_date" in it:
            #     it["last_date"] = it["last_date"].strftime("%Y-%m-%d %H:%M:%S")
            rows.append(it)
        return rows
    except Exception as e:
        LOG.error("资源List加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_delete(ids):
    """
        资源删除

        :param ids: 删除ID
        :return:    响应结果
    """
    try:
        row = 0
        if ids:
            file_name_list = ids.split(",")
            for item in file_name_list:
                rs = Resource.query.filter(Resource.id == item).first()
                if rs:
                    is_exist_children = Resource.query.filter(Resource.parent_code == rs.resource_code).all()
                    if len(is_exist_children) > 0:
                        raise HandleError(ResponseEnum.FAILURE.value, "当前资源[{}]存在子级资源，请先删除所有子级资源！"
                                          .format(rs.resource_code))
                    # 删除关联的表
                    RoleResources.query.filter(RoleResources.resource_code == rs.resource_code).delete()
                    UserResources.query.filter(UserResources.resource_code == rs.resource_code).delete()
                    db.session.delete(rs)
                    db.session.commit()
                    row += 1
        return row
    except HandleError as e:
        LOG.error("删除资源 - 异常：{}".format(e))
        raise e
    except Exception as e:
        LOG.error("删除资源 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_details(id):
    """
        资源详情

        :param id:  主键
        :return:    响应结果
    """
    try:
        return Resource.query.filter(Resource.id == id).first()
    except Exception as e:
        LOG.error("查看资源详情 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_add(resource):
    """
        资源新增

        :param resource:    数据
        :return:        响应结果
    """
    try:
        resource.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        resource.version = 1
        db.session.add(resource)
        db.session.commit()
        return resource
    except Exception as e:
        LOG.error("资源新增 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_edit(resource):
    """
        资源编辑

        :param resource:    数据
        :return:        响应结果
    """
    try:
        # 根据ID查询
        original_resource = Resource.query.filter(Resource.id == resource.id).first()
        original_resource.resource_code = resource.resource_code
        original_resource.resource_level = resource.resource_level
        original_resource.resource_name = resource.resource_name
        original_resource.resource_url = resource.resource_url
        original_resource.describe = resource.describe
        original_resource.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        original_resource.version += 1
        db.session.commit()
        return original_resource
    except Exception as e:
        LOG.error("资源编辑 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_roles_data(resource_code):
    """
        资源角色数据加载

        :param resource_code:   参数
        :return:                resource_name, roles, resource_roles
    """
    try:
        # 1. 查出所有的角色
        roles = Role.query.all()
        # 2. 查出拥有当前资源权限的所有资源角色
        resource = Resource.query.filter(Resource.resource_code == resource_code).first()
        resource_roles = []
        for it in resource.resource_roles.all():
            resource_roles.append({"role_code": it.role_code})
        return resource.resource_name, roles, resource_roles
    except Exception as e:
        LOG.error("资源角色数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_users_data(resource_code):
    """
        资源用户数据加载

        :param resource_code:   参数
        :return:                resource_name, users, resource_users
    """
    try:
        # 1. 查出所有的用户
        users = User.query.all()
        # 2. 查出拥有当前资源权限的所有资源用户
        resource = Resource.query.filter(Resource.resource_code == resource_code).first()
        resource_users = []
        for it in resource.resource_users.all():
            resource_users.append({"user_id": it.id})
        return resource.resource_name, users, resource_users
    except Exception as e:
        LOG.error("资源用户数据加载 - 异常: {}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_roles_save(resource_code, role_codes):
    """
        资源角色保存

        :param resource_code:   资源编号
        :param role_codes:      角色编号List
        :return:                SUCCESS
    """
    try:
        RoleResources.query.filter(RoleResources.resource_code == resource_code).delete()
        role_resources = []
        for role_code in role_codes:
            role_resource = RoleResources(resource_code=resource_code, role_code=role_code,
                                          last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            role_resources.append(role_resource)
        if role_resources:
            db.session.add_all(role_resources)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("资源角色保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def resource_users_save(resource_code, user_ids):
    """
        资源用户保存

        :param resource_code:   资源编号
        :param user_ids:        用户ID List
        :return:                SUCCESS
    """
    try:
        UserResources.query.filter(UserResources.resource_code == resource_code).delete()
        user_resources = []
        for user_id in user_ids:
            user_resource = UserResources(resource_code=resource_code, user_id=user_id,
                                          last_date=datetime.datetime.utcnow() + datetime.timedelta(hours=8))
            user_resources.append(user_resource)
        if user_resources:
            db.session.add_all(user_resources)
        db.session.commit()
        return "SUCCESS"
    except Exception as e:
        LOG.error("资源用户保存 - 异常：{}".format(e))
        raise HandleError(ResponseEnum.FAILURE.value, e)

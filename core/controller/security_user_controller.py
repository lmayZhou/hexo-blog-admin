#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security User Controller
# # -- 用户权限管理
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:40 星期五
# ----------------------------------------------------------
from flask import render_template, request, jsonify
from flask_login import login_required
from core.constant.response_dto import ResponseDTO
from core.constant.response_enum import ResponseEnum
from core.app import app
from core.params.user_query_param import UserQueryParam
from core.handler import security_user_handler
from core.forms.user_form import AddUserForm, ModifyUserForm
from core.models.user import User


@app.route("/admin/security/user.html", methods=["GET"])
@login_required
def user_html():
    """
        用户列表 - 页面

        :return:
    """
    return render_template("security/user.html", title="User List Page")


@app.route("/admin/security/user-<string:operation>.html", methods=["GET"])
@app.route("/admin/security/user-<string:operation>/<int:id>.html", methods=["GET"])
@login_required
def user_edit_html(operation, id=None):
    """
        用户编辑 - 页面

        :return:
    """
    form = AddUserForm()
    if "add" == operation or not id:
        return render_template("security/user-edit.html", title="User Add Page", operation=operation, form=form)
    return render_template("security/user-edit.html", title="User Edit Page", operation=operation, form=form,
                           user=security_user_handler.user_details(id))


@app.route("/admin/security/user-menus/<string:user_id>.html", methods=["GET"])
@login_required
def user_menus_html(user_id):
    """
        用户菜单 - 页面

        :param user_id: 参数
        :return:        视图
    """
    nickname, z_nodes = security_user_handler.user_menus_data(user_id)
    return render_template("security/user-menus.html", title="User Menus Page", user_id=user_id,
                           nickname=nickname, z_nodes=z_nodes)


@app.route("/admin/security/user-resources/<string:user_id>.html", methods=["GET"])
@login_required
def user_resources_html(user_id):
    """
        用户资源 - 页面

        :param user_id: 参数
        :return:        视图
    """
    nickname, z_nodes = security_user_handler.user_resources_data(user_id)
    return render_template("security/user-resources.html", title="User Resources Page", user_id=user_id,
                           nickname=nickname, z_nodes=z_nodes)


@app.route("/admin/security/user-roles/<string:user_id>.html", methods=["GET"])
@login_required
def user_roles_html(user_id):
    """
        用户角色 - 页面

        :param user_id: 参数
        :return:        视图
    """
    nickname, roles, user_roles = security_user_handler.user_roles_data(user_id)
    return render_template("security/user-roles.html", title="User Roles Page", user_id=user_id,
                           nickname=nickname, roles=roles, user_roles=user_roles)


@app.route("/admin/security/user/load", methods=["GET"])
@login_required
def user_load():
    """
        用户列表 - Page

        :return:
    """
    query_param = UserQueryParam()
    query_param.page_number = int(request.args.get("pageNumber") if request.args.get("pageNumber") else 1)
    query_param.page_size = int(request.args.get("pageSize") if request.args.get("pageSize") else 10)
    query_param.sort_name = request.args.get("sortName")
    query_param.sort_order = request.args.get("sortOrder")
    query_param.nickname = request.args.get("nickname") if request.args.get("nickname") else None
    query_param.id = request.args.get("user_id") if request.args.get("user_id") else None
    query_param.sex = request.args.get("sex") if request.args.get("sex") else None
    rs = security_user_handler.user_page(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.__dict__).__dict__)


@app.route("/admin/security/user/list", methods=["GET"])
@login_required
def user_list():
    """
        用户 - List

        :return:
    """
    query_param = UserQueryParam()
    query_param.nickname = request.args.get("nickname") if request.args.get("nickname") else None
    query_param.id = request.args.get("user_id") if request.args.get("user_id") else None
    query_param.sex = request.args.get("sex") if request.args.get("sex") else None
    rs = security_user_handler.user_list(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/user/delete", methods=["POST"])
@login_required
def user_delete():
    """
        用户删除

        :return: 响应结果
    """
    ids = request.form.get('ids')
    rs = security_user_handler.user_delete(ids)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/user/is_disable", methods=["POST"])
@login_required
def user_is_disable():
    """
        是否禁用

        :return: 响应结果
    """
    user_id = request.form.get('id')
    is_available = request.form.get('is_available')
    rs = security_user_handler.user_is_disable(user_id, is_available)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.nickname).__dict__)


@app.route("/admin/security/user/add", methods=["POST"])
@login_required
def user_add():
    """
        用户新增

        :return: 响应结果
    """
    form = AddUserForm()
    # Flask 校验参数
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data, sex=form.sex.data, email=form.email.data, qq=form.qq.data,
                    icon=form.icon.data)
        rs = security_user_handler.user_add(user)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.nickname).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/user/edit", methods=["POST"])
@login_required
def user_edit():
    """
        用户编辑

        :return: 响应结果
    """
    form = ModifyUserForm()
    # Flask 校验参数
    if form.validate_on_submit():
        user = User(id=form.id.data, sex=form.sex.data, email=form.email.data, qq=form.qq.data, icon=form.icon.data)
        rs = security_user_handler.user_edit(user)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.nickname).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/user/menus/save", methods=["POST"])
@login_required
def user_menus_save():
    """
        用户菜单保存

        :return: 响应结果
    """
    user_id = request.form.get("user_id")
    menu_codes = request.form.getlist("menu_codes[]")
    rs = security_user_handler.user_menus_save(user_id, menu_codes)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/user/resources/save", methods=["POST"])
@login_required
def user_resources_save():
    """
        用户资源保存

        :return: 响应结果
    """
    user_id = request.form.get("user_id")
    resource_codes = request.form.getlist("resource_codes[]")
    rs = security_user_handler.user_resources_save(user_id, resource_codes)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/user/roles/save", methods=["POST"])
@login_required
def user_roles_save():
    """
        用户角色保存

        :return: 响应结果
    """
    user_id = request.form.get("user_id")
    role_codes = request.form.getlist("role_codes[]")
    rs = security_user_handler.user_roles_save(user_id, role_codes)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)

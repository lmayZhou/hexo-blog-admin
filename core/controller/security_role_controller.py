#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Role Controller
# # -- 角色权限管理
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
from core.params.role_query_param import RoleQueryParam
from core.handler import security_role_handler
from core.forms.role_form import AddRoleForm, ModifyRoleForm
from core.models.role import Role


@app.route("/admin/security/role.html", methods=["GET"])
@login_required
def role_html():
    """
        角色列表 - 页面

        :return:
    """
    return render_template("security/role.html", title="Role List Page")


@app.route("/admin/security/role-<string:operation>.html", methods=["GET"])
@app.route("/admin/security/role-<string:operation>/<int:id>.html", methods=["GET"])
@login_required
def role_edit_html(operation, id=None):
    """
        角色编辑 - 页面

        :return:
    """
    form = AddRoleForm()
    if "add" == operation or not id:
        return render_template("security/role-edit.html", title="Role Add Page", operation=operation, form=form)
    return render_template("security/role-edit.html", title="Role Edit Page", operation=operation, form=form,
                           role=security_role_handler.role_details(id))


@app.route("/admin/security/role-menus/<string:role_code>.html", methods=["GET"])
@login_required
def role_menus_html(role_code):
    """
        角色菜单 - 页面

        :param role_code:   参数
        :return:            视图
    """
    role_name, z_nodes = security_role_handler.role_menus_data(role_code)
    return render_template("security/role-menus.html", title="Role Menus Page", role_code=role_code,
                           role_name=role_name, z_nodes=z_nodes)


@app.route("/admin/security/role-resources/<string:role_code>.html", methods=["GET"])
@login_required
def role_resources_html(role_code):
    """
        角色资源 - 页面

        :param role_code:   参数
        :return:            视图
    """
    role_name, z_nodes = security_role_handler.role_resources_data(role_code)
    return render_template("security/role-resources.html", title="Role Resources Page", role_code=role_code,
                           role_name=role_name, z_nodes=z_nodes)


@app.route("/admin/security/role-users/<string:role_code>.html", methods=["GET"])
@login_required
def role_users_html(role_code):
    """
        角色用户 - 页面

        :param role_code:   参数
        :return:            视图
    """
    role_name, users, role_users = security_role_handler.role_users_data(role_code)
    return render_template("security/role-users.html", title="Role Users Page", role_code=role_code,
                           role_name=role_name, users=users, role_users=role_users)


@app.route("/admin/security/role/load", methods=["GET"])
@login_required
def role_load():
    """
        角色列表 - Page

        :return:
    """
    query_param = RoleQueryParam()
    query_param.page_number = int(request.args.get("pageNumber") if request.args.get("pageNumber") else 1)
    query_param.page_size = int(request.args.get("pageSize") if request.args.get("pageSize") else 10)
    query_param.sort_name = request.args.get("sortName")
    query_param.sort_order = request.args.get("sortOrder")
    query_param.role_name = request.args.get("role_name") if request.args.get("role_name") else None
    query_param.role_code = request.args.get("role_code") if request.args.get("role_code") else None
    rs = security_role_handler.role_page(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.__dict__).__dict__)


@app.route("/admin/security/role/list", methods=["GET"])
@login_required
def role_list():
    """
        角色 - List

        :return:
    """
    query_param = RoleQueryParam()
    query_param.role_name = request.args.get("role_name") if request.args.get("role_name") else None
    query_param.role_code = request.args.get("role_code") if request.args.get("role_code") else None
    rs = security_role_handler.role_list(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/role/delete", methods=["POST"])
@login_required
def role_delete():
    """
        角色删除

        :return: 响应结果
    """
    ids = request.form.get('ids')
    rs = security_role_handler.role_delete(ids)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/role/add", methods=["POST"])
@login_required
def role_add():
    """
        角色新增

        :return: 响应结果
    """
    form = AddRoleForm()
    # Flask 校验参数
    if form.validate_on_submit():
        role = Role(role_code=form.role_code.data, role_name=form.role_name.data, describe=form.describe.data)
        rs = security_role_handler.role_add(role)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.role_code).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/role/edit", methods=["POST"])
@login_required
def role_edit():
    """
        角色编辑

        :return: 响应结果
    """
    form = ModifyRoleForm()
    # Flask 校验参数
    if form.validate_on_submit():
        role = Role(id=form.id.data, role_code=form.role_code.data, role_name=form.role_name.data,
                    describe=form.describe.data)
        rs = security_role_handler.role_edit(role)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.role_code).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/role/menus/save", methods=["POST"])
@login_required
def role_menus_save():
    """
        角色菜单保存

        :return: 响应结果
    """
    role_code = request.form.get("role_code")
    menu_codes = request.form.getlist("menu_codes[]")
    rs = security_role_handler.role_menus_save(role_code, menu_codes)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/role/resources/save", methods=["POST"])
@login_required
def role_resources_save():
    """
        角色资源保存

        :return: 响应结果
    """
    role_code = request.form.get("role_code")
    resource_codes = request.form.getlist("resource_codes[]")
    rs = security_role_handler.role_resources_save(role_code, resource_codes)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/role/users/save", methods=["POST"])
@login_required
def role_users_save():
    """
        角色用户保存

        :return: 响应结果
    """
    role_code = request.form.get("role_code")
    user_ids = request.form.getlist("user_ids[]")
    rs = security_role_handler.role_users_save(role_code, user_ids)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)

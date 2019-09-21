#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Resource Controller
# -- 资源权限管理
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
from core.params.resource_query_param import ResourceQueryParam
from core.handler import security_resource_handler
from core.forms.resource_form import AddResourceForm, ModifyResourceForm
from core.models.resource import Resource


@app.route("/admin/security/resource.html", methods=["GET"])
@login_required
def resource_html():
    """
        资源列表 - 页面

        :return:
    """
    return render_template("security/resource.html", title="Resource List Page")


@app.route("/admin/security/resource-<string:operation>.html", methods=["GET"])
@app.route("/admin/security/resource-<string:operation>/<int:id>.html", methods=["GET"])
@login_required
def resource_edit_html(operation, id=None):
    """
        资源编辑 - 页面

        :return:
    """
    form = AddResourceForm()
    if "add" == operation or not id:
        return render_template("security/resource-edit.html", title="Resource Add Page", operation=operation, form=form)
    return render_template("security/resource-edit.html", title="Resource Edit Page", operation=operation, form=form,
                           resource=security_resource_handler.resource_details(id))


@app.route("/admin/security/resource-roles/<string:resource_code>.html", methods=["GET"])
@login_required
def resource_roles_html(resource_code):
    """
        资源角色 - 页面

        :param resource_code:   参数
        :return:                视图
    """
    resource_name, roles, resource_roles = security_resource_handler.resource_roles_data(resource_code)
    return render_template("security/resource-roles.html", title="Resource Roles Page", resource_code=resource_code,
                           resource_name=resource_name, roles=roles, resource_roles=resource_roles)


@app.route("/admin/security/resource-users/<string:resource_code>.html", methods=["GET"])
@login_required
def resource_users_html(resource_code):
    """
        资源用户 - 页面

        :param resource_code:   参数
        :return:                视图
    """
    resource_name, users, resource_users = security_resource_handler.resource_users_data(resource_code)
    return render_template("security/resource-users.html", title="Resource Users Page", resource_code=resource_code,
                           resource_name=resource_name, users=users, resource_users=resource_users)


@app.route("/admin/security/resource/load", methods=["GET"])
@login_required
def resource_load():
    """
        资源列表 - Page

        :return:
    """
    query_param = ResourceQueryParam()
    query_param.page_number = int(request.args.get("pageNumber") if request.args.get("pageNumber") else 1)
    query_param.page_size = int(request.args.get("pageSize") if request.args.get("pageSize") else 10)
    query_param.sort_name = request.args.get("sortName")
    query_param.sort_order = request.args.get("sortOrder")
    query_param.parent_code = request.args.get("parent_code") if request.args.get("parent_code") else None
    query_param.resource_name = request.args.get("resource_name") if request.args.get("resource_name") else None
    query_param.resource_code = request.args.get("resource_code") if request.args.get("resource_code") else None
    rs = security_resource_handler.resource_page(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.__dict__).__dict__)


@app.route("/admin/security/resource/list", methods=["GET"])
@login_required
def resource_list():
    """
        资源 - List

        :return:
    """
    query_param = ResourceQueryParam()
    query_param.parent_code = request.args.get("parent_code") if request.args.get("parent_code") else None
    query_param.resource_name = request.args.get("resource_name") if request.args.get("resource_name") else None
    query_param.resource_level = request.args.getlist("resource_level[]") if request.args.getlist("resource_level[]") else None
    query_param.resource_code = request.args.get("resource_code") if request.args.get("resource_code") else None
    rs = security_resource_handler.resource_list(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/resource/delete", methods=["POST"])
@login_required
def resource_delete():
    """
        资源删除

        :return: 响应结果
    """
    ids = request.form.get('ids')
    rs = security_resource_handler.resource_delete(ids)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/resource/add", methods=["POST"])
@login_required
def resource_add():
    """
        资源新增

        :return: 响应结果
    """
    form = AddResourceForm()
    # Flask 校验参数
    if form.validate_on_submit():
        resource = Resource(parent_code=form.parent_code.data, resource_code=form.resource_code.data,
                            resource_level=form.resource_level.data, resource_name=form.resource_name.data,
                            resource_url=form.resource_url.data, describe=form.describe.data)
        rs = security_resource_handler.resource_add(resource)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(
            ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.resource_code).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/resource/edit", methods=["POST"])
@login_required
def resource_edit():
    """
        资源编辑

        :return: 响应结果
    """
    form = ModifyResourceForm()
    # Flask 校验参数
    if form.validate_on_submit():
        resource = Resource(id=form.id.data, parent_code=form.parent_code.data, resource_code=form.resource_code.data,
                            resource_level=form.resource_level.data, resource_name=form.resource_name.data,
                            resource_url=form.resource_url.data, describe=form.describe.data)
        rs = security_resource_handler.resource_edit(resource)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(
            ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.resource_code).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/resource/roles/save", methods=["POST"])
@login_required
def resource_roles_save():
    """
        资源角色保存

        :return: 响应结果
    """
    resource_code = request.form.get("resource_code")
    role_codes = request.form.getlist("role_codes[]")
    rs = security_resource_handler.resource_roles_save(resource_code, role_codes)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/resource/users/save", methods=["POST"])
@login_required
def resource_users_save():
    """
        资源用户保存

        :return: 响应结果
    """
    resource_code = request.form.get("resource_code")
    user_ids = request.form.getlist("user_ids[]")
    rs = security_resource_handler.resource_users_save(resource_code, user_ids)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)

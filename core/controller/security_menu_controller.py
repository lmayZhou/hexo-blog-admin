#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Security Menu Controller
# -- 菜单权限管理
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
from core.params.menu_query_param import MenuQueryParam
from core.handler import security_menu_handler
from core.forms.menu_form import AddMenuForm, ModifyMenuForm
from core.models.menu import Menu


@app.route("/admin/security/menu.html", methods=["GET"])
@login_required
def menu_html():
    """
        菜单列表 - 页面

        :return:
    """
    return render_template("security/menu.html", title="Menu List Page")


@app.route("/admin/security/menu-<string:operation>.html", methods=["GET"])
@app.route("/admin/security/menu-<string:operation>/<int:id>.html", methods=["GET"])
@login_required
def menu_edit_html(operation, id=None):
    """
        菜单编辑 - 页面

        :return:
    """
    form = AddMenuForm()
    if "add" == operation or not id:
        return render_template("security/menu-edit.html", title="Menu Add Page", operation=operation, form=form)
    return render_template("security/menu-edit.html", title="Menu Edit Page", operation=operation, form=form,
                           menu=security_menu_handler.menu_details(id))


@app.route("/admin/security/menu-roles/<string:menu_code>.html", methods=["GET"])
@login_required
def menu_roles_html(menu_code):
    """
        菜单角色 - 页面

        :param menu_code:   参数
        :return:            视图
    """
    menu_name, roles, menu_roles = security_menu_handler.menu_roles_data(menu_code)
    return render_template("security/menu-roles.html", title="Menu Roles Page", menu_code=menu_code,
                           menu_name=menu_name, roles=roles, menu_roles=menu_roles)


@app.route("/admin/security/menu-users/<string:menu_code>.html", methods=["GET"])
@login_required
def menu_users_html(menu_code):
    """
        菜单用户 - 页面

        :param menu_code:   参数
        :return:            视图
    """
    menu_name, users, menu_users = security_menu_handler.menu_users_data(menu_code)
    return render_template("security/menu-users.html", title="Menu Users Page", menu_code=menu_code,
                           menu_name=menu_name, users=users, menu_users=menu_users)


@app.route("/admin/security/menu/load", methods=["GET"])
@login_required
def menu_load():
    """
        菜单列表 - Page

        :return:
    """
    query_param = MenuQueryParam()
    query_param.page_number = int(request.args.get("pageNumber") if request.args.get("pageNumber") else 1)
    query_param.page_size = int(request.args.get("pageSize") if request.args.get("pageSize") else 10)
    query_param.sort_name = request.args.get("sortName")
    query_param.sort_order = request.args.get("sortOrder")
    query_param.parent_code = request.args.get("parent_code") if request.args.get("parent_code") else None
    query_param.menu_name = request.args.get("menu_name") if request.args.get("menu_name") else None
    query_param.menu_code = request.args.get("menu_code") if request.args.get("menu_code") else None
    rs = security_menu_handler.menu_page(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.__dict__).__dict__)


@app.route("/admin/security/menu/list", methods=["GET"])
@login_required
def menu_list():
    """
        菜单 - List

        :return:
    """
    query_param = MenuQueryParam()
    query_param.parent_code = request.args.get("parent_code") if request.args.get("parent_code") else None
    query_param.menu_name = request.args.get("menu_name") if request.args.get("menu_name") else None
    query_param.menu_code = request.args.get("menu_code") if request.args.get("menu_code") else None
    rs = security_menu_handler.menu_list(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/menu/delete", methods=["POST"])
@login_required
def menu_delete():
    """
        菜单删除

        :return: 响应结果
    """
    ids = request.form.get('ids')
    rs = security_menu_handler.menu_delete(ids)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/menu/add", methods=["POST"])
@login_required
def menu_add():
    """
        菜单新增

        :return: 响应结果
    """
    form = AddMenuForm()
    # Flask 校验参数
    if form.validate_on_submit():
        menu = Menu(parent_code=form.parent_code.data, menu_code=form.menu_code.data, menu_name=form.menu_name.data,
                    menu_url=form.menu_url.data, describe=form.describe.data)
        rs = security_menu_handler.menu_add(menu)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.menu_code).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/menu/edit", methods=["POST"])
@login_required
def menu_edit():
    """
        菜单编辑

        :return: 响应结果
    """
    form = ModifyMenuForm()
    # Flask 校验参数
    if form.validate_on_submit():
        menu = Menu(id=form.id.data, parent_code=form.parent_code.data, menu_code=form.menu_code.data,
                    menu_name=form.menu_name.data, menu_url=form.menu_url.data, describe=form.describe.data)
        rs = security_menu_handler.menu_edit(menu)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.menu_code).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@app.route("/admin/security/menu/roles/save", methods=["POST"])
@login_required
def menu_roles_save():
    """
        菜单角色保存

        :return: 响应结果
    """
    menu_code = request.form.get("menu_code")
    role_codes = request.form.getlist("role_codes[]")
    rs = security_menu_handler.menu_roles_save(menu_code, role_codes)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/security/menu/users/save", methods=["POST"])
@login_required
def menu_users_save():
    """
        菜单用户保存

        :return: 响应结果
    """
    menu_code = request.form.get("menu_code")
    user_ids = request.form.getlist("user_ids[]")
    rs = security_menu_handler.menu_users_save(menu_code, user_ids)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)

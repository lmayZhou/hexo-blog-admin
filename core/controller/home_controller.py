#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Home Controller
# -- 门户管理
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:46 星期五
# ----------------------------------------------------------
from flask import request, redirect, url_for, render_template, g, jsonify
from flask_login import current_user, login_required, logout_user, login_user
from core.constant.response_dto import ResponseDTO
from core.constant.response_enum import ResponseEnum
from core.app import app, babel, languages, application, lm
from core.forms.user_form import LoginForm, ModifyUserPasswordForm
from core.models.user import User
from core.utils.security import Security
from core.rbac.rbac_init_permission import RBACInitPermission
from core.handler import security_user_handler
from core.params.modify_password_param import ModifyPasswordParam


@lm.user_loader
def load_user(id):
    """
        load_user 回调

        :param id: User ID
        :return: User
        :rtype: object
    """
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    # 不更新用户修改时间
    # if g.user.is_authenticated():
    #     g.user.last_date = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    #     db.session.add(g.user)
    #     db.session.commit()
    g.locale = get_locale()


@app.route("/admin/login.html", methods=["GET", "POST"])
def login():
    """
        用户登陆

        :return:
    """
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password_key = Security(application["server"]["PRIVATE_KEY"]).encrypt(form.password.data).replace("\n", "")
        user = User.query.filter_by(email=email).first()
        if user and 1 == user.is_available:
            if user.password == password_key:
                user.password = "******"
                # 初始化权限
                RBACInitPermission(user)
                # 保存session
                login_user(user)
                return redirect(url_for("index"))
            else:
                form.password.errors = ("用户密码错误",)
        else:
            if not user:
                form.email.errors = ("用户不存在",)
            else:
                form.email.errors = ("用户已被禁用, 请联系管理员 Email: lmay@lmaye.com",)
        return render_template("login.html", title="Sign In", form=form)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/admin/index.html", methods=["GET"])
@login_required
def index():
    """
        首页

        :return:
    """
    return render_template("index.html", title="Home")


@app.route("/admin/home.html", methods=["GET"])
@login_required
def home():
    """
        Home

        :return:
    """
    return render_template("home.html", title="Home Page")


@app.route("/admin/modify-password/<int:user_id>.html", methods=["GET"])
@login_required
def modify_password_html(user_id):
    """
        密码修改 - 视图

        :param user_id: 用户ID
        :return:        视图
    """
    form = ModifyUserPasswordForm()
    return render_template("user/modify_password.html", title="User Modify Password Page", form=form, user_id=user_id)


@app.route("/admin/modify-password", methods=["POST"])
@login_required
def modify_password():
    """
        密码修改

        :return:    响应结果
    """
    form = ModifyUserPasswordForm()
    if form.validate_on_submit():
        param = ModifyPasswordParam(id=form.id.data, old_password=form.old_password.data, password=form.password.data,
                                    confirm_password=form.confirm_password.data)
        rs = security_user_handler.modify_password(param)
        success_value = ResponseEnum.SUCCESS.value
        return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.nickname).__dict__)
    validate_error = ResponseEnum.PARAM_VALIDATE_ERROR.value
    return jsonify(ResponseDTO(code=validate_error["code"], msg=validate_error["msg"], data=form.errors).__dict__)


@babel.localeselector
def get_locale():
    """
        国际化与本地化

        :return:
    """
    return request.accept_languages.best_match(languages.keys())


@app.route("/admin/logout")
def logout():
    # 清空session
    logout_user()
    return redirect(url_for("login"))

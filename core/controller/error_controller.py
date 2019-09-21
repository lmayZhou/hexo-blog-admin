#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Error Views
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月28日 16:23:47
# ----------------------------------------------------------
from core.app import app, db
from core.exception.custom_errors import HandleError, VerifyError
from flask import render_template, jsonify


@app.errorhandler(403)
def internal_error(e):
    """
        访问权限

        :param e:
        :return:
    """
    return render_template('error-page/403.html', title="403"), 403


@app.errorhandler(404)
def internal_error(e):
    """
        资源不可访问

        :param e:
        :return:
    """
    return render_template('error-page/404.html', title="404"), 404


@app.errorhandler(500)
def internal_error(e):
    """
        服务异常

        :param e:
        :return:
    """
    db.session.rollback()
    return render_template('error-page/500.html', title="500"), 500


@app.errorhandler(VerifyError)
def verify_error_handler(e):
    """
        校验异常

        :param e:   异常信息
        :return:    反馈响应
    """
    return jsonify(e.responseDTO.__dict__)


@app.errorhandler(HandleError)
def handle_error_handler(e):
    """
        全局处理异常

        :param e:   异常信息
        :return:    反馈响应
    """
    return jsonify(e.responseDTO.__dict__)

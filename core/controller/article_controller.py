#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Article Controller
# -- 文章管理 - 视图层
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:40 星期五
# ----------------------------------------------------------
import time
import requests
from flask import render_template, jsonify, request, json
from flask_login import login_required
from core.app import app, application, csrf
from core.constant.response_dto import ResponseDTO
from core.constant.response_enum import ResponseEnum
from core.forms.md_editor_forms import MDEditorForm
from core.handler import article_handler
from core.params.article_query_param import ArticleQueryParam


@app.route("/admin/articles.html", methods=["GET"])
@login_required
def articles_html():
    """
        文章列表 - 页面

        :return:
    """
    return render_template("user/articles.html", title="Article List Page")


@app.route("/admin/article/<string:operation>.html", methods=["GET"])
@app.route("/admin/article/<string:operation>/<string:file_name>.html", methods=["GET"])
def article_html(operation=None, file_name=None):
    """
        文章详情 - 页面

        :param operation: 操作
        :param file_name: 文件名
        :return:
    """
    form = MDEditorForm()
    return render_template("user/article-edit.html", title="Article Edit Page", form=form, operation=operation,
                           file_name=file_name)


@app.route("/admin/articles/load", methods=["GET"])
@login_required
def load_articles():
    """
        文章列表 - 数据

        TODO 分页[数据量大时，使用此方法提升性能]:
            {_id: {"$lt": "20180629002015"}}    分页起始值，根据最小值排除
            sort({"_id": -1})                   根据ID倒叙
            limit(3)                            分页数量
        db.getCollection('articles').find({_id: {"$lt": "20180629002015"}}).sort({"_id": -1}).limit(3)

        :return:
    """
    query_param = ArticleQueryParam()
    query_param.page_number = int(request.args.get("pageNumber") if request.args.get("pageNumber") else 1) - 1
    query_param.page_size = int(request.args.get("pageSize") if request.args.get("pageSize") else 10)
    query_param.sort_name = request.args.get("sortName")
    query_param.sort_order = request.args.get("sortOrder")
    query_param.author = request.args.get("author") if request.args.get("author") else None
    rs = article_handler.load_articles(query_param)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs.__dict__).__dict__)


@app.route("/admin/article/edit.md", methods=["POST"])
@login_required
def article_edit():
    """
        文章编辑

        :return:
    """
    form = MDEditorForm()
    _file_name = form.file_name.data
    editor_txt = form.editor_txt.data
    if not _file_name or "None" == _file_name:
        _file_name = time.strftime('%Y%m%d%H%M%S', time.localtime())
    article_handler.edit_article(editor_txt, _file_name)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data="/admin/articles.html").__dict__)


@app.route("/admin/article/delete", methods=["POST"])
@login_required
def article_delete():
    """
        文章删除

        :return: 响应结果
    """
    file_names = request.form.get('file_names')
    rs = article_handler.delete_article(file_names)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/article/load/<string:file_name>.md", methods=["GET"])
@login_required
def article_md(file_name):
    """
        文章Markdown 数据加载

        :param file_name: 文件名
        :return:
    """
    rs = article_handler.read_article(file_name)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/about-me.html", methods=["GET"])
@login_required
def about_me_html():
    """
        关于我 - 页面

        :return:
    """
    form = MDEditorForm()
    return render_template("user/about-me.html", title="About Me Page", form=form)


@app.route("/admin/about-me/edit.md", methods=["POST"])
@login_required
def about_me_edit():
    """
        关于我 - 编辑

        是否提交: if form.validate_on_submit():
        :return:
    """
    form = MDEditorForm()
    editor_txt = form.editor_txt.data
    rs = article_handler.modify_about_me(editor_txt)
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@app.route("/admin/about-me/load.md", methods=["GET"])
@login_required
def about_me_md():
    """
        关于我Markdown 数据加载

        :return:
    """
    rs = article_handler.read_about_me()
    success_value = ResponseEnum.SUCCESS.value
    return jsonify(ResponseDTO(code=success_value["code"], msg=success_value["msg"], data=rs).__dict__)


@csrf.exempt
@app.route("/admin/api/img/upload", methods=["POST"])
@login_required
def img_upload():
    """
        图片上传

        {
            success : 0 | 1, //0表示上传失败;1表示上传成功
            message : "提示的信息",
            url     : "图片地址" //上传成功时才返回
        }

        :return: Markdown 格式
    """
    data = {"enctype": "multipart/form-data"}
    headers = {
        "Authorization": "Token",
        "Client-ID": "www.lmaye.com",
        "User-Name": "lmayZhou"
    }
    image_file = request.files['editormd-image-file']
    files = {"file": (image_file.filename, image_file)}
    response = requests.post(application["file-api"]["upload"], data=data, headers=headers, files=files)
    rs = json.loads(response.content.decode("UTF-8"))
    if 200 != response.status_code or 200 != rs["code"]:
        return jsonify({"success": 0, "message": rs["message"], "url": ""})
    return jsonify({"success": 1, "message": rs["msg"], "url": application["file-api"]["localhost"] + rs["data"]})

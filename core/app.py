#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This"s python application controller
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月13日 09:45:13
# ----------------------------------------------------------
from flask import Flask
from flask_babel import Babel, lazy_gettext
from flask_login import LoginManager
from flask_mail import Mail
from flask_minio import Minio
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from core.constant.sys_enum import SysEnum
from core.utils.momentjs import momentjs
from core.utils.pub_utils import CustomJSONEncoder
from core.utils import read_config
from core.rbac.rbac_middleware import RBACMiddleware


"""
    Flask:
    
    static_url_path   静态资源
    static_folder     静态资源路径
    template_folder   HTML路径
"""
app = Flask(__name__, static_url_path="/static", static_folder="../resources/static",
            template_folder="../resources/templates")
application = read_config.read_yml(SysEnum.APPLICATION_PATH.value)
rbac_whitelist = application["rbac"]["whitelist"]
flask_wtf = application["flask"]["wtf"]
app.config.from_mapping(flask_wtf)
csrf = CSRFProtect(app)
# Use Databases
server_conf = application["server"]
databases = server_conf["databases"]
db_yml = read_config.read_yml(SysEnum.DB_PATH.value)
databases_obj = db_yml[databases]
if databases == "mysql":
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://" + databases_obj["user"] + ":" + databases_obj["password"] + "@" \
                                            + databases_obj["host"] + ":" + str(databases_obj["port"]) + "/" \
                                            + databases_obj["database"] + "?charset=" + databases_obj["charset"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + SysEnum.RESOURCES_PATH.value + SysEnum.SEPARATOR.value \
                                            + databases_obj["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = databases_obj["SQLALCHEMY_TRACK_MODIFICATIONS"]
db = SQLAlchemy(app)

# MongoDB
mongo = db_yml["mongo"]
app.config.from_mapping(mongo)
mongo_db = PyMongo(app)

# Moment JS
app.jinja_env.globals["momentjs"] = momentjs

# 登录拦截
lm = LoginManager()
lm.init_app(app)
lm.login_view = "/admin/login.html"
lm.login_message = lazy_gettext('Please log in to access this page.')
lm.login_message_category = "info"

# Email Server
email = application["email"]
app.config.from_mapping(email)
mail = Mail(app)

# 国际化和本地化
languages = server_conf["LANGUAGES"]
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "../resources/translations"
babel = Babel(app)
app.json_encoder = CustomJSONEncoder

# RBAC 权限拦截
app.before_request(RBACMiddleware.rbac_middleware)

# File Api(文件存储服务)
use_file_api = server_conf["use_file_api"]
file_api = application["file-api"]
api_conf = file_api[use_file_api]
if "minio" == use_file_api:
    app.config.from_mapping(api_conf)
    minio_storage = Minio(app)

# Models 导入
from core.models import user, role, menu, resource, role_menus, role_resources, user_roles, user_menus, user_resources

# Views 导入
from core.controller import error_controller, home_controller, article_controller, security_menu_controller, \
    security_resource_controller, security_role_controller, security_user_controller

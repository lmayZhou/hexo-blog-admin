#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 
# ----------------------------------------------------------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\\Workspaces\\Python\\hexo-blog-admin\\resources\\app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from bin import user, role, menu, resource, role_menus, role_resources, user_roles, user_menus, user_resources
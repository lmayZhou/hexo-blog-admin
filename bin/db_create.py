#!flask/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Create Databases
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月13日 17:16:06
# ----------------------------------------------------------
import os
from bin.app import db
from migrate.versioning import api

db.create_all()
SQLALCHEMY_DATABASE_URI = 'sqlite:///E:\\Workspaces\\Python\\hexo-blog-admin\\resources\\app.db'
# SQLALCHEMY_DATABASE_URI = 'mysql://root:root@192.168.31.11:3306/hexo-blog-admin?charset=utf8mb4'
SQLALCHEMY_MIGRATE_REPO = 'E:\\Workspaces\\Python\\hexo-blog-admin\\resources\\db_repository'
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, "database repository")
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                        api.version(SQLALCHEMY_MIGRATE_REPO))

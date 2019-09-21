#!flask/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Migrate Databases
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月26日 15:53:05
# ----------------------------------------------------------
import imp
from bin.app import db
from migrate.versioning import api

SQLALCHEMY_DATABASE_URI = 'sqlite:///E:\\Workspaces\\Python\\hexo-blog-admin\\resources\\app.db'
# SQLALCHEMY_DATABASE_URI = 'mysql://root:root@192.168.31.11:3306/hexo-blog-admin?charset=utf8mb4'
SQLALCHEMY_MIGRATE_REPO = 'E:\\Workspaces\\Python\\hexo-blog-admin\\resources\\db_repository'

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v + 1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)

script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))

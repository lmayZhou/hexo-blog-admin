#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Editor Form
# -- 
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/29 1:21 星期日
# ----------------------------------------------------------
from flask_wtf import FlaskForm as Form
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired


class MDEditorForm(Form):
    file_name = StringField("file_name", validators=[DataRequired()])
    editor_txt = TextAreaField("editor_txt", validators=[DataRequired()])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Role Forms
# -- 角色Form表单
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:45 星期五
# ----------------------------------------------------------
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddRoleForm(Form):
    """
        AddRoleForm

        -- add role
    """
    role_code = StringField("Role Code", validators=[DataRequired(message="[Role Code] This field is required."),
                                                     Length(4, 32)])
    role_name = StringField("Role Name", validators=[DataRequired(message="[Role Name] This field is required."),
                                                     Length(2, 64)])
    describe = TextAreaField("Describe", validators=[DataRequired(message="[Describe] This field is required."),
                                                     Length(2, 255)])


class ModifyRoleForm(Form):
    """
        ModifyRoleForm

        -- modify role
    """
    id = StringField("ID", validators=[DataRequired(message="[ID] This field is required.")])
    role_code = StringField("Role Code", validators=[DataRequired(message="[Role Code] This field is required."),
                                                     Length(4, 32)])
    role_name = StringField("Role Name", validators=[DataRequired(message="[Role Name] This field is required."),
                                                     Length(2, 64)])
    describe = TextAreaField("Describe", validators=[DataRequired(message="[Describe] This field is required."),
                                                     Length(2, 255)])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Menu Forms
# -- 菜单Form表单
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:45 星期五
# ----------------------------------------------------------
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddMenuForm(Form):
    """
        Add Menu Form

        -- add menu
    """
    parent_code = StringField("Parent Code", validators=[DataRequired(message="[Parent Code] This field is required."),
                                                         Length(1, 32)])
    menu_code = StringField("Menu Code", validators=[DataRequired(message="[Menu Code] This field is required."),
                                                     Length(4, 32)])
    menu_name = StringField("Menu Name", validators=[DataRequired(message="[Menu Name] This field is required."),
                                                     Length(2, 64)])
    menu_url = StringField("Menu URL", validators=[DataRequired(message="[Menu URL] This field is required."),
                                                   Length(1, 255)])
    describe = TextAreaField("Describe", validators=[DataRequired(message="[Describe] This field is required."),
                                                     Length(2, 255)])


class ModifyMenuForm(Form):
    """
        Modify Menu Form

        -- modify menu
    """
    id = StringField("ID", validators=[DataRequired(message="[ID] This field is required.")])
    parent_code = StringField("Parent Code", validators=[DataRequired(message="[Parent Code] This field is required."),
                                                         Length(1, 32)])
    menu_code = StringField("Menu Code", validators=[DataRequired(message="[Menu Code] This field is required."),
                                                     Length(4, 32)])
    menu_name = StringField("Menu Name", validators=[DataRequired(message="[Menu Name] This field is required."),
                                                     Length(2, 64)])
    menu_url = StringField("Menu URL", validators=[DataRequired(message="[Menu URL] This field is required."),
                                                   Length(1, 255)])
    describe = TextAreaField("Describe", validators=[DataRequired(message="[Describe] This field is required."),
                                                     Length(2, 255)])

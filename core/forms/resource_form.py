#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Resource Forms
# -- 资源Form表单
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:45 星期五
# ----------------------------------------------------------
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class AddResourceForm(Form):
    """
        AddResourceForm

        -- add resource
    """
    parent_code = StringField("Parent Code", validators=[DataRequired(message="[Parent Code] This field is required."),
                                                         Length(1, 32)])
    resource_code = StringField("Resource Code",
                                validators=[DataRequired(message="[Resource Code] This field is required."),
                                            Length(4, 32)])
    resource_level = IntegerField("Resource Level", validators=[
        NumberRange(min=0, max=2, message="数值范围已超出(eg: 0-2)")])
    resource_name = StringField("Resource Name",
                                validators=[DataRequired(message="[Resource Name] This field is required."),
                                            Length(2, 64)])
    resource_url = StringField("Resource URL",
                               validators=[DataRequired(message="[Resource URL] This field is required."),
                                           Length(1, 255)])
    describe = TextAreaField("Describe", validators=[DataRequired(message="[Describe] This field is required."),
                                                     Length(2, 255)])


class ModifyResourceForm(Form):
    """
        ModifyResourceForm

        -- modify resource
    """
    id = StringField("ID", validators=[DataRequired(message="[ID] This field is required.")])
    parent_code = StringField("Parent Code", validators=[DataRequired(message="[Parent Code] This field is required."),
                                                         Length(1, 32)])
    resource_code = StringField("Resource Code", validators=[
        DataRequired(message="[Resource Code] This field is required."), Length(4, 32)])
    resource_level = IntegerField("Resource Level", validators=[
        NumberRange(min=0, max=2, message="数值范围已超出(eg: 0-2)")])
    resource_name = StringField("Resource Name", validators=[
        DataRequired(message="[Resource Name] This field is required."), Length(2, 64)])
    resource_url = StringField("Resource URL", validators=[
        DataRequired(message="[Resource URL] This field is required."), Length(1, 255)])
    describe = TextAreaField("Describe", validators=[DataRequired(message="[Describe] This field is required."),
                                                     Length(2, 255)])

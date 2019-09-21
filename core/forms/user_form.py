#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This"s User Forms
# -- 用户Form表单
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/20 0:45 星期五
# ----------------------------------------------------------
from flask_wtf import FlaskForm as Form
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, NumberRange


class AddUserForm(Form):
    """
        AddUserForm

        -- add user
    """
    nickname = StringField("Nickname", validators=[DataRequired(message="[Nickname] This field is required."),
                                                   Length(2, 64)])
    email = StringField("Email", validators=[Length(0, 64), Email(message="邮箱地址格式有误")])
    sex = IntegerField("Sex", validators=[NumberRange(min=0, max=2, message="性别格式有误")])
    icon = StringField("Icon", validators=[Length(0, 255)])
    qq = StringField("QQ", validators=[Regexp(regex="^[1-9][0-9]{4,11}$", message="QQ格式有误")])


class ModifyUserForm(Form):
    """
        ModifyUserForm

        -- modify user
    """
    id = StringField("Id", validators=[DataRequired(message="[Id] This field is required.")])
    nickname = StringField("Nickname", validators=[DataRequired(message="[Nickname] This field is required."),
                                                   Length(2, 64)])
    email = StringField("Email", validators=[Length(0, 64), Email(message="邮箱地址格式有误")])
    sex = IntegerField("Sex", validators=[NumberRange(min=0, max=2, message="性别格式有误")])
    icon = StringField("Icon", validators=[Length(0, 255)])
    qq = StringField("QQ", validators=[Regexp(regex="^[1-9][0-9]{4,11}$", message="QQ格式有误")])


class ModifyUserPasswordForm(Form):
    """
        ModifyUserPasswordForm

        -- modify user password
    """
    id = StringField("Id", validators=[DataRequired(message="[Id] This field is required.")])
    old_password = PasswordField("Old Password", validators=[
        DataRequired(message="[Old Password] This field is required."), Length(8, 64)])
    password = PasswordField("Password", validators=[DataRequired(message="[Password] This field is required."),
                                                     Length(8, 64)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="[Confirm Password] This field is required."),
        EqualTo("password", message="Passwords must match"), Length(8, 64)])


class LoginForm(Form):
    """
        LoginForm

        -- This"s the user login.
    """
    email = StringField("Email", validators=[DataRequired(message="[Email] This field is required.")])
    password = StringField("Password", validators=[DataRequired(message="[Password] This field is required.")])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Email Util
# --
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年3月2日 12:23:29
# ----------------------------------------------------------
from flask import render_template
from flask_mail import Message
from core.app import mail, app, email
from core.utils.decorators import i_async


@i_async
def send_async_email(obj, msg):
    """
        Send Async Email
        -- 异步发送邮件

        :param obj: obj
        :param msg: msg
        :return:    None
    """
    with obj.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
        Send Email
        -- 发送邮件

        :param subject:     主题
        :param sender:      寄件人
        :param recipients:  收件人
        :param text_body:   plain text message
        :param html_body:   HTML message
        :return:            None
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


def user_add_notification(user, password):
    """
        User Add Notification
        -- 用户注册初始密码提醒

        :param user:        user
        :param password:    password
    """
    send_email("欢迎加入 [lmayZhou's Blog]", email["MAIL_USERNAME"], [user.email],
               render_template("email/user_add_email.txt", nickname=user.nickname, email=user.email, password=password),
               render_template("email/user_add_email.html", nickname=user.nickname, email=user.email, password=password))

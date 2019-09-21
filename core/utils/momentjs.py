#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Moment JS
# -- Moment.js 是一个小型的，自由的，开源的 Javascript 库，它能够渲染日期和时间。
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年3月6日 17:13:30
# ----------------------------------------------------------
from flask import g
from jinja2 import Markup


class momentjs(object):
    """
        Moment JS

        moment.locale(\"%s\"); 全局国际化和本地化
        -- Moment.js 是一个小型的，自由的，开源的 Javascript 库，它能够渲染日期和时间。
    """
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\n moment.locale(\"%s\");\n document.write(moment(\"%s\").%s);\n</script>" %
                      (g.locale, self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")

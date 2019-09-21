#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's python application main
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月13日 09:45:18
# ----------------------------------------------------------
from core.app import app, application

if __name__ == "__main__":
    # 开发环境
    app.run(host="127.0.0.1", debug=True, port=application["server"]["port"])
    # 正式环境
    # app.run(host="127.0.0.1", port=application["server"]["port"])

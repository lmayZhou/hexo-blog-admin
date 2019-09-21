#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Response Enum
# -- 响应常量枚举值
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年7月2日 15:10:50
# ----------------------------------------------------------
from enum import Enum, unique


@unique
class ResponseEnum(Enum):
    """
        Response Enum
    """
    SUCCESS = {"code": 200, "msg": "处理成功"}
    FAILURE = {"code": -105, "msg": "处理失败"}
    TYPE_ERROR = {"code": -106, "msg": "类型不支持"}
    PARAM_VALIDATE_ERROR = {"code": -107, "msg": "参数校验失败"}

    UNAUTHORIZED = {"code": 401, "msg": "未经授权"}
    FORBIDDEN = {"code": 403, "msg": "资源不可用"}
    NOT_FOUND = {"code": 404, "msg": "页面不存在"}
    SERVER_ERROR = {"code": 500, "msg": "服务器内部错误"}

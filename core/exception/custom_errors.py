#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Custom Exception
# -- 自定义异常
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/7/2 14:56 星期一
# ----------------------------------------------------------
from core.constant.response_dto import ResponseDTO


class VerifyError(Exception):
    """
        - 校验异常
    """
    def __init__(self, response_enum, data):
        super().__init__(self, data)
        # 响应对象
        self.responseDTO = ResponseDTO(code=response_enum["code"], msg=response_enum["msg"], data=data)


class HandleError(Exception):
    """
        - 处理异常
    """
    def __init__(self, response_enum, *args):
        super().__init__(self, args)
        # 响应对象
        self.responseDTO = ResponseDTO(code=response_enum["code"], msg=response_enum["msg"], data=str(args[0]))


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Encrypt、Decrypt
# -- 采用AES对称加密算法
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018年4月18日 11:07:00
# ----------------------------------------------------------
import base64
from Crypto.Cipher import AES


class Security(object):
    def __init__(self, key):
        # 秘钥
        self.key = key
        self.mode = AES.MODE_ECB

    @staticmethod
    def to_sixteen(value):
        """
            str不是16的倍数那就补足为16的倍数

            :param value: value
            :return: bytes
        """
        while len(value) % 16 != 0:
            value += "\0"
        return str.encode(value)

    def encrypt(self, text):
        """
            内容加密

            :param text: text
            :return: encrypt text
        """
        # 初始化加密器
        aes = AES.new(self.to_sixteen(self.key), self.mode)
        # 先进行aes加密
        encrypt_aes = aes.encrypt(self.to_sixteen(text))
        # 用base64转成字符串形式
        return str(base64.encodebytes(encrypt_aes), encoding="utf-8")

    def decrypt(self, text):
        """
            内容解密

            :param text: text
            :return: decrypt text
        """
        # 初始化加密器
        aes = AES.new(self.to_sixteen(self.key), self.mode)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding="utf-8"))
        # 执行解密密并转码返回str
        return str(aes.decrypt(base64_decrypted), encoding="utf-8")

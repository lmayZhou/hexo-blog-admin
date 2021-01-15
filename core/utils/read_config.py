#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Read Config File
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月13日 10:05:28
# ----------------------------------------------------------
import json
import yaml
from core import LOG


def read_json(path=None):
    """
        This's read JSON config file.

        :param path: JSON config file path.
        :type path: str or None
        :return: JSON object
        :rtype: object
    """
    if path:
        with open(path, "r", encoding="UTF-8") as js:
            return json.loads(js.read())
    else:
        LOG.error("JSON config file path is None ...")
        return None


def read_yml(path=None):
    """
        This's read yml config file.

        :param path: Yml config file path.
        :type path: str or None
        :return: Yml object
        :rtype: object
    """
    if path:
        with open(path, "r", encoding="UTF-8") as yml:
            return yaml.load(yml.read(), yaml.Loader)
    else:
        LOG.error("yml config file path is None ...")
        return None

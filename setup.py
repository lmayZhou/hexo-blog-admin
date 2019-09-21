#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 
# -- 打包命令: python setup.py sdist
# -- pip可以直接安装dist下的压缩包,代码：pip3 install zsf-test-1.0.0.tar.gz
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Email lmay@lmaye.com
# Date: 2018/4/28 12:35 星期六
# ----------------------------------------------------------
import setuptools
import textwrap
from setuptools import find_packages

if __name__ == "__main__":
    setuptools.setup(
        name="hexo-blog-admin",
        version="1.0.0",
        description="lmayZhou Blog Admin",
        author="lmay",
        author_email="lmay@lmaye.com",
        long_description=textwrap.dedent("""hexo-blog-admin"""),
        packages=find_packages(),
        install_requires=[
            "Flask",
            "xmltodict",
        ],
        include_package_data=True,
        zip_safe=False,
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- OSS文件上传
# --
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2021/1/21 11:15
# Email lmay@lmaye.com
# ----------------------------------------------------------
import sys
import uuid
from pathlib import Path
from minio import Minio


minio_storage = Minio("192.168.30.180:9000", access_key='admin', secret_key='YouGuess', secure=False)
images = sys.argv[1:]
for image in images:
    print("File Uploading ...")
    suffix = Path(image).suffix
    file_name = str(uuid.uuid4()) + suffix
    minio_storage.fput_object("hexo-blog", file_name, image, content_type="image/png",
                              part_size=10485760)
    print("http://192.168.30.180/files/hexo-blog/{}".format(file_name))

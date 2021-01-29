#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- OSS文件上传
# -- Typora工具脚本
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

# access_key: MinIo帐号
# secret_key: MinIo密码
minio_storage = Minio("192.168.30.180:9000", access_key="admin", secret_key="YouGuess", secure=False)
images = sys.argv[1:]
for image in images:
    print("File Uploading ...")
    suffix = Path(image).suffix
    file_name = str(uuid.uuid4()) + suffix
    # 存储桶名称
    bucket_name = "hexo-blog"
    if not minio_storage.bucket_exists(bucket_name):
        # 如果存储桶不存在，则创建
        minio_storage.make_bucket(bucket_name)
    minio_storage.fput_object(bucket_name, file_name, image, content_type="image/png", part_size=10485760)
    print("http://192.168.30.180/files/{}/{}".format(bucket_name, file_name))

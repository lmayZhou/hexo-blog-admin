### 一.  介绍

​	本章主要讲述的是通过**Typora** + **Python** 脚本来实现**Typora** 工具编辑Markdown文件时的图片上传处理。通过Docker部署Nginx，MinIO容器，Nginx代理访问MinIO资源。

效果如下：

![1](http://192.168.30.180/files/hexo-blog/0200e4e7-857a-4e35-a470-06094553615b.gif)

### 二. 相关脚本

​	以下是相关服务及脚本实例。

#### 1. Python3

```python
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

# access_key: MinIo帐号
# secret_key: MinIo密码
minio_storage = Minio("192.168.30.180:9000", access_key='admin', secret_key='YouGuess', secure=False)
images = sys.argv[1:]
for image in images:
    print("File Uploading ...")
    suffix = Path(image).suffix
    file_name = str(uuid.uuid4()) + suffix
    # 存储桶名称
    bucket_name = "hexo-blog"
    minio_storage.fput_object(bucket_name, file_name, image, content_type="image/png", part_size=10485760)
    print("http://192.168.30.180/files/{}/{}".format(bucket_name, file_name))
```

#### 2. Nginx 配置

```properties
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;

events {
worker_connections  1024;
}

http {
include       mime.types;
default_type  application/octet-stream;

#log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
#                  '$status $body_bytes_sent "$http_referer" '
#                  '"$http_user_agent" "$http_x_forwarded_for"';

#access_log  logs/access.log  main;

sendfile        on;
#tcp_nopush     on;

#keepalive_timeout  0;
keepalive_timeout  65;

#gzip  on;

server {
listen       80;
server_name  localhost;

#charset koi8-r;

#access_log  logs/host.access.log  main;

#location / {
#    root   html;
#    index  index.html index.htm;
#}

#location / {
#    proxy_pass http://spring-boot-elasticsearch:60;
#    proxy_set_header Host $host;
#    # proxy_set_header X-Forwarded-Host $server_name;
#    proxy_set_header X-Real-IP $remote_addr;
#    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#}

#error_page  404              /404.html;

# redirect server error pages to the static page /50x.html
#
error_page   500 502 503 504  /50x.html;
location = /50x.html {
root   html;
}

# proxy the PHP scripts to Apache listening on 127.0.0.1:80
#
#location ~ \.php$ {
#    proxy_pass   http://127.0.0.1;
#}

# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
#
#location ~ \.php$ {
#    root           html;
#    fastcgi_pass   127.0.0.1:9000;
#    fastcgi_index  index.php;
#    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
#    include        fastcgi_params;
#}

# deny access to .htaccess files, if Apache's document root
# concurs with nginx's one
#
#location ~ /\.ht {
#    deny  all;
#}

# 配置MinIO资源
# http://192.168.30.180/files/hexo-blog/287872bb-f461-4abe-8ce0-aaac09db1633.png
location ^~ /files/ {
root /usr/share/nginx/html;
}
}
}
```

#### 3. Docker Compose

```yaml
version: "3"
services:
  nginx:
    container_name: blog-nginx
    image: nginx:1.16
    restart: on-failure
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./nginx/www:/usr/share/nginx/html
      - ./nginx/conf/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/logs:/var/log/nginx

  minio:
    # 容器名称
    container_name: blog-minio
    # 镜像:版本
    image: minio/minio:latest
    # 重启机制
    # -- no: 禁止自动重启容器(默认);
    # -- always: 无论如何容器都会重启;
    # -- on-failure: 当出现on-failure报错时, 容器重新启动;
    restart: on-failure
    command: server /data
    # 端口
    ports:
      - 9000:9000
    environment:
      MINIO_ACCESS_KEY: admin
      MINIO_SECRET_KEY: YouGuess
    # 持久化挂载
    volumes:
      # Nginx代理访问资源
      - ./nginx/www/files:/data
      - ./minio/conf:/root/.minio
```

### 三. Typora配置

#### 1. Python脚本测试：

​	CMD命令：

```shell
E:\md>python oss_upload.py "C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210121112644841.png"
File Uploading ...
http://192.168.30.180/files/hexo-blog/7dd6ea8a-551c-48dc-baba-e3506e52556a.gif
```

#### 2. Typora工具配置

​	**配置步骤：**文件 -> 偏好设置 -> 图像

​	**如下所示**

​	**命令：**python oss_upload.py（Python脚本没有写觉得路径，因为我把脚本放在了MD文件目录下）

![image-20210121152155883](http://192.168.30.180/files/hexo-blog/f07e368c-0e74-4ac5-8f1c-fae3fb98abc0.png)
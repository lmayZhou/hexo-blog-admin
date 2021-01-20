#!/bin/bash
. /etc/profile

#########################################
## 宿主机部署项目，可直接项目来执行此脚本  ##
#########################################
cd /home/lmay/blog/hexo-blog/

hexo g

\cp -af /home/lmay/blog/hexo-blog/public/* /usr/local/nginx-1.13.7/html/lmayZhou/

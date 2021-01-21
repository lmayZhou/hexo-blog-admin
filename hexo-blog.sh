#!/bin/bash
. /etc/profile

#########################
## hexo 生成静态页面脚本  ##
#########################
cd /home/lmay/blog/hexo-blog/

hexo g

\cp -af /home/lmay/blog/hexo-blog/public/* /usr/local/nginx-1.13.7/html/lmayZhou/

#!/bin/bash
. /etc/profile

cd /home/lmay/blog/hexo-blog/

hexo g

\cp -af /home/lmay/blog/hexo-blog/public/* /home/lmay/services/blog/nginx/www/lmayZhou

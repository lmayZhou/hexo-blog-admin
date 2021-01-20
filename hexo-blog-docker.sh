#!/bin/bash
. /etc/profile

####################################################
## Docker部署项目容器资源隔离，过定时任务来触发此脚本  ##
####################################################
# 将文章MD文件，复制到生成的hexo站点静态项目目录中
\cp -af /home/services/hexo-blog/hexo-blog-admin/resources/source/_posts/* /home/services/hexo-blog/source/_posts/
# 切换到hexo站点目录
cd /home/services/hexo-blog
# 生成页面
hexo g
# 将静态页面复制到nginx中
\cp -af /home/services/hexo-blog/public/* /home/services/hexo-blog/nginx/www/lmayZhou/

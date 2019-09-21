# Hexo Blog Admin(Python 3.6版本)

#### 项目介绍
```text
####################################################
#             >>> Blog 初始账户 <<<                #
#            用户: lmay@lmaye.com                  #
#            密码: root@123                        #
####################################################
```
&emsp;&emsp;Hexo Blog Admin 基于 Python3 编写的Hexo博客后台管理系统。由于本人不善于前端UI特效编写，所以博客前端采用Hexo主题模版，
还有一个原因是Hexo的Admin版本效果不是很好，故使用Python Flask框架开发出一套可供Hexo主题和读取Markdown文件的博客后台管理系统；
※ 本项目开源，仅供学习参考与个人使用！如有更好的方案和idea，欢迎互相交流！如您觉得该项目对您有所帮助，欢迎点击右上方的Star标记，给予支持！！！谢谢 ~ ~

#### 项目结构
&emsp;&emsp;Python项目结构并非如此，由于本人比较喜欢Java项目结构，故此项目结构参考的Java项目，但Python不建议层次结构太深，所以最终简化为以下结构；

    hexo-blog-admin                         # Hexo Blog Admin
        - core                              # 核心代码
            -- constant                     # 常量
            -- controller                   # 控制器
            -- exception                    # 自定义异常
            -- forms                        # Form表单实体
            -- handler                      # 业务处理层
            -- logger                       # 日志
            -- models                       # 实体
            -- params                       # 参数
            -- rbac                         # RBAC访问权限控制
            -- utils                        # 工具类
            __init__.py                     # 初始化文件
            app.py                          # APP应用
        -- resources                        # 项目资源目录
            -- db_repository                # 数据库生成资源目录[已生成，可忽略]
            -- docs                         # 文档目录
            -- source                       # Markdown文件目录[仅供测试]
            -- static                       # 静态文件目录（js/css/images...）
            -- templates                    # HTML文件目录
            app.db                          # sqlite数据库
            application.yml                 # 项目配置文件
            databases.yml                   # 数据库配置文件
            logging.conf                    # 日志配置文件
        - bin                               # 执行脚本[可忽略]
        - logs                              # 日志目录
        hexo-blog.sh                        # 生成静态页面脚本
        hexo-blog-admin.ini                 # uwsgi配置文件（web服务器）
        requirements.txt                    # 批量安装关联插件
        run.py                              # 应用启动
        setup.py                            # 应用打包[可忽略]
        README.md                           # 项目文档

### 系统架构
![Hexo Blog Admin](https://www.lmaye.com/group1/M00/00/00/CmiBTl1K9TKAYEd8AACaQc7nGPU158.png "Hexo Blog Admin")

&emsp;&emsp;系统应用基于Python Flask框架开发，系统访问权限控制使用的RBAC实现，国际化由于时间关系所以也没有实现，博客基本需求是完全可以满足的。   
文件存储服务没有使用第三方服务，而是自己搭建了FastDFS文件服务系统，因为Python调用FastDFS存在各种问题，从而采用的Java编写的API服务（由于存在个人隐私，源码陆续开放，敬请期待），TODO: 后续也会继续优化支持多种方式。   
前端采用的Markdown插件，编辑完成后会生成MD文件，MongoDB仅仅存储文章的基本信息和路径，不会去存储文章内容；同时也支持MongoDB数据恢复，故MongoDB服务挂了造成数据丢失也不必担心；   
Security系统管理数据存储在Sqlite DB中，之所以采用Sqlite是因为这部分数据量不是很大，仅仅存储用户、菜单、资源、权限等数据；
其他细节部分，大家可以自己参考源码；

### 注意事项
   1. 安装项目集成插件
```shell
pip3 install flask
pip3 install pyyaml
pip3 install flask_wtf
pip3 install flask_sqlalchemy
pip3 install flask_mail
pip3 install flask-login==0.2.11
pip3 install flask_babel
# 翻译lazy字符串
pip3 install speaklater
# Crypto 加密
pip3 install pycryptodome
# Redis
pip3 install flask-redis
# MongoDB
pip3 install Flask-PyMongo==0.5.2
# RABC 权限框架
pip3 install flask-rbac
pip3 install flask-marshmallow
# 接口请求
pip3 install requests
```
   
   2. 解决安装pycryptodome加密插件引入的问题，\Lib\site-packages\crypto(crypto默认是小写，改成大写即可Crypto)
   
   3. [完善] 批量安装
```shell
pip3 install -r requirements.txt
```
   
   4. 项目启动命令
```shell
# 启动项目
uwsgi --ini hexo-blog-admin.ini
# 查看进程
ps aux | grep uwsgi
# 停止项目
killall -9 uwsgi
```

### 参与贡献
1. 2018年04月15日: 初始化项目
2. 2018年09月05日: 完成项目
3. 2018年11月11日: 首页添加时间轴
4. 2019年08月07日: 更新 README.md [文档]

### 相关文章
#### 『 Hexo 相关资料』
- [Hexo 主题模版](https://hexo.io/)

#### 『 Centos 7 快速教程 』
- [Centos 7 静态IP设置](https://www.lmaye.com/2017/12/22/20180809103359/)
- [Linux增加bash脚本为service，开机自启服务脚本配置](https://www.lmaye.com/2017/12/23/20180809103413/)
- [Centos7 安装 Docker CE](hhttps://www.lmaye.com/2019/04/28/20190428183357/)
- [Centos7 安装 JDK1.8](https://www.lmaye.com/2019/04/29/20190429005630/)
- [Centos7 安装较高版本Ruby2.2+（RVM 安装）](https://www.lmaye.com/2019/01/24/20190124223042/)
- [Centos7 开启Docker远程API访问端口](https://www.lmaye.com/2019/06/04/20190604230713/)

#### 『 Docker 快速教程 』
- [Docker 安装 MongoDB](https://www.lmaye.com/2019/05/06/20190506232452/)
- [Docker 安装 MySQL 8.0](https://www.lmaye.com/2019/05/22/20190522162930/)
- [Dockerfile 部署MySql 8并初始化数据脚本](https://www.lmaye.com/2019/06/02/20190602133656/)

#### 『 Redis 快速教程 』
- [Redis 配置文件详解](https://www.lmaye.com/2018/09/06/20180906002632/)
- [Redis Cluster 集群](https://www.lmaye.com/2019/01/24/20190124212849/)
- [Redis 配置集群遇到问题及解决方法](https://www.lmaye.com/2019/01/24/20190124223656/)

#### 『 FastDFS 快速教程 』
- [FastDFS 搭建文件管理系统](https://www.cnblogs.com/chiangchou/p/fastdfs.html)

### 联系我
    * QQ: 379839355
    * QQ群: [Æ┊Java✍交流┊Æ](https://jq.qq.com/?_wv=1027&k=5Dqlg2L)
    * QQ群: [Cute Python](https://jq.qq.com/?_wv=1027&k=58hW2jl)
    * Email: lmay@lmaye.com
    * Home: [lmaye.com](https://www.lmaye.com)
    * GitHub: [lmayZhou](https://github.com/lmayZhou)

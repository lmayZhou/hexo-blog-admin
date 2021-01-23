最简单的部署Python项目操作，部署比较简单这块也不做详细描述了。基本上都是常规命令~ ~

这些东西基本上都可以灵活运用到其他地方，不仅仅只适用于此项目~ ~

### 1 更换Centos源

由于系统默认使用国外的源更新软件时太慢，所以更换为国内的更新源。

**阿里云的源**

```shell
[root@localhost ~]# wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo 
```

**网易云的源**

```shell
[root@localhost ~]# wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo
[root@localhost ~]# yum makecache
```

### 2 Python3配置

#### 2.1 安装Python3

```shell
# 下载Python3.7
[root@localhost ~]# wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
# 解压
[root@localhost ~]# tar -xvf Python-3.7.0.tar.xz 
[root@localhost ~]# cd Python-3.7.0
# 更新
[root@localhost ~]# yum update -y
# 安装Python3.7的依赖
[root@localhost ~]# yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gcc make
# 将python安装到/usr/local/python3
[root@localhost ~]# ./configure --prefix=/usr/local/python3
# 编译并安装
[root@localhost ~]# make && make install
# 建立python3软连接
[root@localhost ~]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
# 建立pip3软连接
[root@localhost ~]# ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3
# 更新升级pip3
[root@localhost ~]# pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
# 将/usr/local/python3/bin加入PATH
[root@localhost ~]# vi /etc/profile
# 在文件末尾添加
export PATH=$PATH:/usr/local/python3/bin
# 环境变量在配置信息中生效
[root@localhost ~]# source /etc/profile
```

#### 2.2 Python3.x 设置默认

```shell
# 修改yum配置
[root@localhost ~]# vi /usr/bin/yum
将第一行 #! /usr/bin/python 修改为#! /usr/bin/python2
# 修改urlgrabber-ext-down配置
[root@localhost ~]# vi /usr/libexec/urlgrabber-ext-down
将第一行 #! /usr/bin/python 修改为#! /usr/bin/python2
# 删除原有的软连接
[root@localhost ~]# rm -rf /usr/bin/python
# 建立新的软连接
[root@localhost ~]# ln -s /usr/local/python3/bin/python3 /usr/bin/python
# 查看版本
[root@localhost ~]# python
Python 3.7.0 (default, Jan 23 2021, 02:55:09) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
# 修改pip软连接
[root@localhost ~]# rm -rf /usr/bin/pip
# 建立新的pip软连接
[root@localhost ~]# ln -s /usr/bin/pip3 /usr/bin/pip
# 安装uWSGI服务
[root@localhost ~]# pip install uWSGI==2.0.18
# 建立新的uwsgi软连接(下面自启脚本会用到)
[root@localhost ~]# ln -s /usr/local/python3/bin/uwsgi  /usr/bin/uwsgi
```

#### 2.3 安装docker-compose

```shell
# 安装docker-compose
[root@localhost ~]# curl -L https://github.com/docker/compose/releases/download/1.26.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
[root@localhost ~]# chmod +x /usr/local/bin/docker-compose
[root@localhost ~]# ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 安装依赖工具bash-complete
[root@localhost ~]# yum install -y bash-completion
[root@localhost ~]# source /usr/share/bash-completion/completions/docker
[root@localhost ~]# source /usr/share/bash-completion/bash_completion
```

### 3 uwsgi开机自启服务

创建hexo-blog-admin.service [Centos服务脚本]文件，按下面操作即可。

```shell
# 1.进入脚本目录
[root@localhost ~]# cd /lib/systemd/system/
# 2.创建脚本
[root@localhost ~]# vi hexo-blog-admin.service
# 虚线表示文件中的配置
------------------------------------------------------------------------------------------------
[Unit]
# 脚本描述
Description=hexo-blog-admin
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
# 启动uwsgi(/home/lmay/services/blog/hexo-blog-admin/hexo-blog-admin.ini 脚本根据自己实际位置调整)
ExecStart=/usr/bin/uwsgi /home/lmay/services/blog/hexo-blog-admin/hexo-blog-admin.ini
# 停止uwsgi
ExecStop=killall -9 uwsgi
Restart=always
PrivateTmp=true

[Install]
WantedBy=multi-user.target
------------------------------------------------------------------------------------------------
# 3.设置脚本开机自启
[root@localhost ~]# systemctl enable hexo-blog-admin.service
# 4.常用命令
重新加载service文件：	systemctl daemon-reload
启动一个服务：systemctl start xxx.service
关闭一个服务：systemctl stop xxx.service
重启一个服务：systemctl restart xxx.service
显示一个服务的状态：systemctl status xxx.service
在开机时启用一个服务：systemctl enable xxx.service
在开机时禁用一个服务：systemctl disable xxx.service
查看服务是否开机启动：systemctl is-enabled xxx.service
查看已启动的服务列表：systemctl list-unit-files|grep enabled
查看启动失败的服务列表：systemctl --failed
```

### 4 docker-compose部署相关依赖服务

docker更简单了，脚本基本上已经写好。一键执行即可~~

因为直接把写好的init.sh复制到Linux下，不知道为啥不能正常执行。故直接手动在Linux中创建一个init.sh脚本，然后把写好的命令直接复制过去即可。

```shell
# 创建脚本
[root@localhost ~]# vi init.sh
# 脚本授权
[root@localhost ~]# chmod 777 init.sh
# 查看文件
[root@nacos blog]# ll
total 24
# 自动部署脚本
-rwxrwxrwx 1 root root 1978 Jan 23 03:07 init.sh
# 核心文件(直接复制过来即可)
-rw-r--r-- 1 root root 2095 Jan 23 03:05 docker-compose.yml
# 项目放置,随心所欲(项目中的一些配置,根据自己实际情况调整)
drwxr-xr-x 7 root root 4096 Jan 23 04:36 hexo-blog-admin
# 部署依赖服务
[root@nacos blog]# ./init.sh
# 等执行完成即可
...
...
...
```


### 5 Docker Nginx代理宿主机服务

安装Docker时会在宿主机安装一个虚拟网关 docker0

```shell
# 查询docker0的IP地址
[root@localhost ~]# ip addr show docker0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:55:33:a8:24 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever

# 配置docker上安装的nginx
    server {
        listen 80;
        server_name www.lmaye.com;
        location / {
            # 设置最大允许上传单个的文件大小
            client_max_body_size 100m;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            # 反向代理到宿主机服务
            proxy_pass http://172.17.0.1:8080;
        }
    }
```

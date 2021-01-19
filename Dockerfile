FROM python:3.9
ENV TZ=Asia/Shanghai
# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
RUN mkdir /webapp
WORKDIR /webapp
ADD . /webapp
#RUN apk add --no-cache gcc musl-dev linux-headers
# 安装模块
RUN pip3 install -r requirements.txt
CMD [ "uwsgi", "--ini", "hexo-blog-admin.ini" ]

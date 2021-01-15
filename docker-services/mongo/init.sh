#!/bin/bash

# 定义颜色
BLUE_COLOR="\033[36m"
RED_COLOR="\033[31m"
GREEN_COLOR="\033[32m"
VIOLET_COLOR="\033[35m"
RES="\033[0m"

echo -e "${BLUE_COLOR}# ######################################################################${RES}"
echo -e "${BLUE_COLOR}#                       Docker Compose Shell Script                    #${RES}"
echo -e "${BLUE_COLOR}#                       Blog: www.lmaye.com                            #${RES}"
echo -e "${BLUE_COLOR}#                       Email: lmay@lmaye.com                          #${RES}"
echo -e "${BLUE_COLOR}# ######################################################################${RES}"

# 创建目录
echo -e "${BLUE_COLOR}---> create [logs & tracker & storage]directory start.${RES}"
if [ ! -d "./logs/" ]; then
mkdir -p ./logs
fi
if [ ! -d "./data/" ]; then
mkdir -p ./data
fi
echo -e "${BLUE_COLOR}===> create directory success.${RES}"
echo -e "${GREEN_COLOR}>>>>>>>>>>>>>>>>>> The End <<<<<<<<<<<<<<<<<<${RES}"

# 部署项目
echo -e "${BLUE_COLOR}==================> Docker deploy Start <==================${RES}"
docker-compose up --build -d

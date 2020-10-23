#!/bin/bash

# red='\e[91m'
# green='\e[92m'
# yellow='\e[93m'
# magenta='\e[95m'
# cyan='\e[96m'
# none='\e[0m'

echo -e "正在获取工作路径。。"
workpath=$(pwd)
pwd > ./config/path
echo -e "获取成功：" $yellow $workpath $none

echo -e "欢迎尝试今日校园自动签到，此部署脚本"$red"没有"$none"进行"$red"输入验证"$none", 请不要输入奇怪的东西。同意请继续："
echo -e $green"1. 同意"
echo -e $red"2. 非常同意"$none
read -p "请输入： 1 或 2:" result
if test $result -eq 1
then 
    echo -e "非常好！让我们继续吧！"
elif test $result -eq 2
then 
    echo -e "非常好！让我们继续吧！"
else
    echo -e $red"Bye."
    exit 1
fi

py3=$(which python3)
if test -z $py3
then
    echo -e $red"没有安装python3，请安装后再运行。 apt-get install python3"
fi

echo -e $none "准备录入必备信息："
python3 generate_config.py
echo -e $red"准备登陆"$none
python3 login.py
echo -e $red"准备第一次签到验证"$none
python3 index_sign.py
echo -e $red"正在注册自动化任务"$none
echo "0,50 9 * * * python3 "$workpath"/index_sign.py >> "$workpath"/sign.log" > timedTask
crontab timedTask


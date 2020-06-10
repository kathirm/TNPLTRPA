#!/bin/sh
path=$(pwd)
echo "Hi Welcome"
#python $path'/uI_service.py' &
#python $path'/api_service.py' &
python /home/centos/selfservice/uI_service.py &
python /home/centos/selfservice/api_service.py &


#https://www.tecmint.com/auto-execute-linux-scripts-during-reboot-or-startup/

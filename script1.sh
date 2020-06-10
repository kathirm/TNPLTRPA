#!/bin/bash
DATE=$(date +'%F %H:%M:%S')
echo "welcome Odoo"
DIR=/home/centos/selfservice
python  $DIR/uI_service.py &
python  $DIR/api_service.py &
python  $DIR/base_subscription.py &


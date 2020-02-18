#!/bin/sh
path=$(pwd)
echo "Hi Welcome"
python $path'/uI_service.py' &
python $path'/api_service.py' &


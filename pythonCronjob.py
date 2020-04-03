#!/usr/bin/env python

from time import sleep 
from apscheduler.schedulers.background import BackgroundScheduler



scheduler = BackgroundScheduler()
scheduler.start()

# define the function that is to be executed
def my_job():
    print "HIO"


job = scheduler.add_job(my_job, 'cron', hour='11', minute='25', second='00') 
print "Cron job starting....."
while True:
    sleep(45)

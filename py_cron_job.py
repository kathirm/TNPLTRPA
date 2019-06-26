import schedule
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

print "Execution time ::", datetime.datetime.now().strftime("%I:%M:%S %p")

sched = BlockingScheduler() 

def job():
    curtime = datetime.datetime.now().strftime("%I:%M:%S %p")
    print "i'm working & Time:: %s"%curtime

def hi():
    print "Hi david"

def job_month():
    print "HI im month function"

schedule.every(1).minutes.do(job)
schedule.every().hour.do(hi)
schedule.every().day.at("00:00").do(hi)
        
while 1:    
    schedule.run_pending()
    time.sleep(1)

sched.add_job(job_month, 'cron', month='1-12', hour='0')

sched.start()

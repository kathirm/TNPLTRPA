import os, time, sys
import pymongo
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from kafka import KafkaConsumer, KafkaProducer
from mongodb.mongolib import MongoLib
from common.utils import *
import json
import logging
import ConfigParser


if __name__ == "__main__":

    #if len(sys.argv) != 3:
    #    print "Usage: %s <kafkaIp:kafkaPort> <qName to poll>" % (sys.argv[0])
    #    sys.exit(0);
    bootstrapServer = "10.6.4.36:9092"  #sys.argv[1];
    inJobsQName = "003"   #sys.argv[2]
    producer = KafkaProducer(bootstrap_servers=bootstrapServer)

    consumer = KafkaConsumer(inJobsQName, bootstrap_servers=bootstrapServer);
    print "Waiting for messages.... QueueName :: %s"%(inJobsQName)
    for job in consumer:
        print job#.value
    
#    try:
        # This is here to simulate application activity (which keeps the main thread alive).
#        while True:
#           time.sleep(2)
#    except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
#        scheduler.shutdown()

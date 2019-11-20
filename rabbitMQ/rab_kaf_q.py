import os, time, sys
from apscheduler.schedulers.background import BackgroundScheduler
from kafka import KafkaConsumer, KafkaProducer
import pika

def callback(msg):
    try:
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='', routing_key='hello', body=job_value)

    except Exception as er:
        print("\n [WARNING] callback function exception :: %s"%er)



if __name__ == "__main__":

    bootstrapServer = "10.6.4.36:9092"
    inJobsQName = "geoAttendance"
    producer = KafkaProducer(bootstrap_servers=bootstrapServer)
    consumer = KafkaConsumer(inJobsQName, bootstrap_servers=bootstrapServer);
    print("waiting for messages....")

    for job in consumer: 
        job_value = job.value
        callback(job_value)





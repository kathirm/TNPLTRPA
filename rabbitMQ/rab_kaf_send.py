import json, sys, os
from kafka import SimpleProducer, KafkaClient
import json, pika

sample= {
        'imageMatch': 'true',
        'fileName':'thilagaTest'
        }
kafka = KafkaClient('10.6.4.36:9092')
producer = SimpleProducer(kafka)

data = json.dumps(sample)
producer.send_messages(b'geoAttendance', data)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body=data)
print(" [x] Sent 'done.....!!!'")
connection.close()


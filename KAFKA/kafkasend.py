from kafka import SimpleProducer, KafkaClient
import json 

sample= { 
        'imageMatch': True,
        'fileName':'M.Ravichandran.1.jpg'
    }

kafka = KafkaClient('10.6.4.36:9092')
producer = SimpleProducer(kafka)
data = json.dumps(sample)
producer.send_messages(b'003', data)


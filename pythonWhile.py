import time
import os
import paho.mqtt.client as mqtt
starttime=time.time()

broker_url = "localhost"
broker_port = 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

while True:
    print "Send Response Done....!"
    client.publish(topic="TestingTopic", payload="TestingPayload", qos=1, retain=False)
    time.sleep(1 - ((time.time() - starttime) %1))

    

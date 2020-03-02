import time, json
import paho.mqtt.client as mqtt
starttime=time.time()

broker_url = "localhost"
broker_port = 1883


client = mqtt.Client()
client.connect(broker_url, broker_port)
Init = 0

while True:
    Init = Init + 1
    data = {"Responce" : Init}
    print "Send Response Done....!" + str(data)
    client.publish(topic="TestingTopic", payload = json.dumps(data), qos=1, retain=False)
    time.sleep(1 - ((time.time() - starttime) %1))

    

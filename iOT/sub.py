import paho.mqtt.client as mqtt
import time
broker_url = "10.6.0.14"
broker_port = 1883
starttime=time.time()

def on_connect(client, userdata, flags, rc):    
    print("Connected With Result Code "+rc)

def on_message(client, userdata, message):
    print("Message Recieved: "+message.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)
client.subscribe("humidTemp", qos=1)
client.publish(topic = "humidTemp", payload="TestingPayload", qos=1, retain=False)
client.loop_forever()

import paho.mqtt.client as mqtt

broker_url = "host"
broker_port = 1883

def on_message(client, userdata, message):
    print("Message Recieved: "+message.payload.decode())


if __name__ == "__main__":
    
    client = mqtt.Client()
    print "Mqtt Connection :: %s && Waiting for Msg"%client
    client.on_message = on_message
    client.connect(broker_url, broker_port)
    client.subscribe("TestingTopic", qos=1)
    client.loop_forever()

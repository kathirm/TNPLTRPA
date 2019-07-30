import paho.mqtt.client as mqtt

hostname = "10.7.0.14"
port = 1883

def on_message(client, obj, msg):

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


if __name__ == "__main__":

    mqttc = mqtt.Client()
    mqttc.on_message = on_message

    mqttc.connect(hostname, port)
    mqttc.subscribe('Auth_Q', qos=1)
    rc = 0
    while rc == 0:
        rc = mqttc.loop()

import json, os
import paho.mqtt.client as mqtt






if __name__ == "__main__":  

    data = {
                  "deviceId" : "VFDI001",
                  "cardId" : "22458",
                  "timestamp" : "2019-07-02 16:48:27",
                  "inTime" : "10.30AM",
                  "outTime" : "18.00PM"
                }
                                                                                        
    client = mqtt.Client()
    client.connect("10.6.0.14" , 1883)    
    client.subscribe("Auth_Q", qos=1)
    client.publish(topic = "Auth_Q", payload=json.dumps(data), qos=1, retain=False)


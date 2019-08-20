import paho.mqtt.client as mqtt
import datetime, json
import requests

broker_url = "10.6.0.12"
broker_port = 1883


def on_connect(client, userdata, flags, rc):

    print("Connected With Result Code"+rc)

def on_message(client, userdata, message):
    #print("Message Recieved: "+message.payload.decode())
    getData = message.payload.decode().split(":")
    time = getData[2]

    timeStamp = datetime.datetime.fromtimestamp(int(time)).strftime('%d-%m-%Y %H:%M:%S')
    attd_dict = {}
    attd_dict["deviceID"] = getData[0]
    attd_dict["CardID"] = getData[1]
    attd_dict["time"] = timeStamp
    attd_dict["Type"] = getData[3]
    print attd_dict
    token = login(attd_dict)   #LogIn Credentials
    entryAttnd = inputAttdEntry(attd_dict, token)
    
def login(attnd_dict):
    try:
        userName  = "Terafast"
        Password  = "!changeme!"
        token = None;
        login_url = "http://controller:8080/auth/login?username=Admin@%s&password=%s" %(userName, Password)
        headers = []
        token = requests.get(login_url, headers)
        if token.text is not None:
            token_dict= json.loads(token.text)
            if 'access-token' in token_dict:
                token = token_dict['access-token']
                print "retrived token for the user " + userName + " with token: " + token
    except Exception as er:
        print "Login function Exception error :: %s"%er

    return token

def inputAttdEntry(inputData, token):
    try:
        headers = {"Authorization" : "Bearer %s " %token, "Content-Type":"application/json"}
        getuId = inputData['CardID']
        chktime = inputData['time']
        EntryType = inputData['Type']
        if EntryType == "IN":            
            gen_url = "http://controller:8080/attendance?uId=%s&checkin=%s"%(getuId, chktime)
            print "CheckIn URL :: %s"%gen_url
            resp = requests.post(gen_url, headers=headers);
            print "Employee CheckIn HttpResponse :: %s"%resp
        else:
            gen_url = "http://controller:8080/attendance?uId=%s&checkout=%s"%(getuId, chktime)
            print "CheckIn URL :: %s"%gen_url
            resp = requests.post(gen_url, headers=headers);
            print "Employee CheckIn HttpResponse :: %s"%resp

    except Exception as er:
        print "inputAttndEntry Exception as error :: %s"%er

if __name__ == "__main__":
    
    client = mqtt.Client()
    print "Mqtt Connection :: %s && Waiting for Msg"%client
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_url, broker_port)
    client.subscribe("FinPrint_Q", qos=1)
    client.publish(topic="FinPrint_Q", payload="Test", qos=1, retain=False)
    client.loop_forever()

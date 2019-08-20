#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import json, time, calendar
from datetime import date
import paho.mqtt.client as mqtt

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        exit(0)
    else:       
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        intData = {}
        print "Today",d1
        intData["fingerID"] = positionNumber;
        intData["Date"] = d1;
        intData[d1] = "IN"; 
        with open("search.json", 'r') as mydata:
            searchdata = json.load(mydata)
            listLen = len(searchdata)
            print "FileLength", listLen
        if listLen == 0:            
            searchdata.append(intData)
            intf = json.dumps(searchdata)
            with open('search.json', 'w') as intfile:
                 intfile.write(intf)
                 tType = "IN"
        else: 
            for i in searchdata:   
                getDat =  i.get(d1)
                getId =  i.get("fingerID")
                getDate  = i.get("Date")

                if getDate == d1 and getId == positionNumber:
                    tType = "OUT" 
                    break
                #else:
                #    print "%s Record Not Found"%(d1)

            if getDat is None:
                searchdata.append(intData)
                intf = json.dumps(searchdata)                    
                with open("search.json", 'w') as myfile:                        
                    myfile.write(intf)
                    tType = "IN"
                 
            elif getId != positionNumber and getDate == d1:                               
                searchdata.append(intData)
                intf = json.dumps(searchdata)
                with open("search.json", "w") as elfile:                    
                    elfile.write(intf)
                tType = "IN"

            else:  
                if i["fingerID"] == positionNumber:                                                
                    typ = i[d1]                   
                    if typ == "IN":
                        tType = "OUT"
                    else:
                        tType = "IN"                 
        ChkType = tType

        with open("data.json", 'r') as myfile:
            dat = json.load(myfile)
            ti = int(time.time())
            ts = ti + 000;
            for _id in dat:
                get_id = _id["fingerID"]
                if _id["fingerID"] == positionNumber:
                    empName = _id["EmpName"]
                    uId =  _id["uId"] 
                    variable = "fp:%s:%s:%s:%s"%(uId, ts, ChkType, empName)
                    print variable
                    client = mqtt.Client()
                    client.connect("10.7.0.12" , 1883)
                    client.subscribe("FinPrint_Q", qos=1)
                    client.publish(topic = "FinPrint_Q", payload=variable, qos=1, retain=False)
            
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))

    ## OPTIONAL stuff
    ##

    ## Loads the found template to charbuffer 1
    f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    ## Hashes characteristics of template
    print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)

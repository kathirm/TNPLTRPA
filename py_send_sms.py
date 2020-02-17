from twilio.rest import Client
import string, time
import random

def otp():
    try:
        chars = string.digits;
        password = ''
        for i in range(4):
            password += random.choice(chars)
    except Exception as eR:
        print "OTP Generation exception eror: %s"%eR

    return password

def sms_integ():
    try:
        account_sid = 'ACeb5fcef2905d61dd58713018059ba3b3'
        auth_token = 'a0adb50e5537cd8bba07907891c37ace'
        
        #T = "+919566540187"
        #B = "+919600099520"
        J = "+918870653018"
        #R = "+919884055194" UR
        #CR = "+919791020409" UR
        #K = "+918940776800"
        #Y = "+919791305251"
        client = Client(account_sid, auth_token)
        #print "client_connection_status", client
        password = otp()
        message = client.messages.create(
                body  ='Hi...! Welcome to Terafast Networks RPA Portal-Access Login OTP : '+password+' Thank you :)',
                from_ = '+12564729952',
                to    = J 
                )
        print(message.sid)       
        print "OTP send Successfully for Registed PhoneNumber"
        #time.sleep(20)
        print "OTP Session Expired"
    except Exception as er:
        print er

sms_integ()

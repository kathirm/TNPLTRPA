import requests
import json


def pyCurl_whatsappInteg():

    try:
        account_sid = 'AC0f74e11b97e0f09228efec8d7845a4c5';
        auth_token = '5224ddc36583ef88f620f32bee5067bf';
        body = "Hi"
        print "whatsapp Connection request id = %s & token %s"%(account_sid, auth_token)

        gen_url_token = 'curl' +' ' + 'https://api.twilio.com/2010-04-01/Accounts/' + account_sid + '/Messages.json' "-X POST  --data-urlencode 'To=whatsapp:+918940776800' --data-urlencode 'From=whatsapp:+14155238886'" +' '+ '--data-urlencode' +' '+"'" + 'Body='+ body + "!'" + ' '+ '-u '  + account_sid+':'+auth_token
        print gen_url_token
        #get_to_Num = "--data-urlencode 'To=whatsapp:+918940776800'"
        #get_from_Num = "--data-urlencode 'From=whatsapp:+14155238886'"
        #get_body = "--data-urlencode 'Body= %s. '"%(body)
        #get_acc_token = " -u %s:%s"%(account_sid, auth_token)        

        result = requests.post(gen_url_token) 
               
        print result

    except Exception as er:
        print er

pyCurl_whatsappInteg()

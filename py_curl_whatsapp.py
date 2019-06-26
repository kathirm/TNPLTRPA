import requests
import json


def pyCurl_whatsappInteg():

    try:
        account_sid = 'xxxxxxxxxxxxxxxxx';
        auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxx';
        body = "Hi"
        print "whatsapp Connection request id = %s & token %s"%(account_sid, auth_token)

        gen_url_token = 'curl' +' ' + 'https://api.twilio.com/2010-04-01/Accounts/' + account_sid + '/Messages.json' "-X POST  --data-urlencode 'To=whatsapp:+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' --data-urlencode 'From=whatsapp:+xxxxxxxxxxxxxxxxxxxxxxxxxx'" +' '+ '--data-urlencode' +' '+"'" + 'Body='+ body + "!'" + ' '+ '-u '  + account_sid+':'+auth_token
        print gen_url_token
        #get_to_Num = "--data-urlencode 'To=whatsapp:+xxxxxxxxxxx'"
        #get_from_Num = "--data-urlencode 'From=whatsapp:+xxxxxxxxxxxxxxx'"
        #get_body = "--data-urlencode 'Body= %s. '"%(body)
        #get_acc_token = " -u %s:%s"%(account_sid, auth_token)        

        result = requests.post(gen_url_token) 
               
        print result

    except Exception as er:
        print er

pyCurl_whatsappInteg()

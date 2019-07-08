from twilio.rest import Client

def sms_integ():
    try:
        account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx';
        auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

        client = Client(account_sid, auth_token)
        print "client_connection_status", client

        message = client.messages.create(
                body  ='Hello there!',
                from_ ='+12523022064',
                to    ='+918015978503'
                )
        print(message.sid)

    except Exception as er:
        print er

sms_integ()

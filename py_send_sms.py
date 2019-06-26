from twilio.rest import Client

def sms_integ():
    try:
        account_sid = 'AC0f74e11b97e0f09228efec8d7845a4c5';
        auth_token = '5224ddc36583ef88f620f32bee5067bf'

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

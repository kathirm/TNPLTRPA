from twilio.rest import Client


def whatsapp_integ():

    try:
        account_sid = 'xxxxxxxxxxxx';
        auth_token = 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'

        client = Client(account_sid, auth_token)
        print "client_connection_status", client

        message = client.messages.create(
                body  ='Hello there!',
                from_ ='whatsapp:+14155238886',
                to    ='whatsapp:+918015978503'
                )
        print(message.sid)

    except Exception as er:
        print er

whatsapp_integ() 


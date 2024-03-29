# python script for sending message update 

import time
import sys
from time import sleep 
from sinchsms import SinchSMS 

# function for sending SMS 
def sendSMS(): 

	# enter all the details 
	# get app_key and app_secret by registering 
	# a app on sinchSMS
        # e0dfdf4e51b248bdbb0b8fbdaa5948e8
        #b1b93f20210d4ca3945eb5a8710f80e3

	number = sys.argv[1] 
	app_secret = '' 
	app_key = ''

	# enter the message to be sent 
	message = 'Hello Message!!!'

	client = SinchSMS(app_key, app_secret) 
	print("Sending '%s' to %s" % (message, number)) 

	response = client.send_message(number, message) 
	message_id = response['messageId'] 
	response = client.check_status(message_id) 

	# keep trying unless the status retured is Successful 
	while response['status'] != 'Successful': 
		print(response['status']) 
		time.sleep(1) 
		response = client.check_status(message_id) 

	print(response['status']) 

if __name__ == "__main__": 
	sendSMS() 

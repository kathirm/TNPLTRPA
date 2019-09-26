import os
import slack

client = slack.WebClient(token=os.environ['xoxp-746486182899-745176922162-757967863712-802567eee6ea96ae68381611077bc0e6'])

response = client.chat_postMessage(
        channel='#rpa',
        text="Hello world!")
assert response["ok"]
assert response["message"]["text"] == "Hello world!"

import os
import slack
import asyncio

loop = asyncio.get_event_loop()

client = slack.WebClient(        
        token=os.environ['xoxp-746486182899-745176922162-757967863712-802567eee6ea96ae68381611077bc0e6'],
        run_async=True)

response = loop.run_until_complete(client.chat_postMessage(    
    channel='#rpa',    
    text="Hello world!"
            )
                                    )
assert response["ok"]
assert response["message"]["text"] == "Hello world!"

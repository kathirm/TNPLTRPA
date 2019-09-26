from slackclient import SlackClient

slack_token = os.environ["xoxp-746486182899-745176922162-757967863712-802567eee6ea96ae68381611077bc0e6"]
sc = SlackClient(slack_token)

sc.api_call(
          "chat.postMessage",
            channel="#rpa",
              text="Hello from Python! :tada:"
              )

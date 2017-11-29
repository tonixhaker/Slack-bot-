from slackclient import SlackClient

slack_token = "xoxp-278627039044-278509049315-279267478244-7cecdc08ca2b7ec6a497c985b15526d2"
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#general",
  text="Hello from Python! :tada:"
)
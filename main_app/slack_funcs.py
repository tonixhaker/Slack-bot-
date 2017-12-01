import slackweb
from slackclient import SlackClient

def HookSend(message):
    slack_client = SlackClient(message.team.bot_access_token)
    users = slack_client.api_call("users.list")
    for user in users['members']:
        if user['id']==message.user_id:
            sender = user
            break
    name = sender['real_name']
    nick = sender['id']

    hook = message.team.incoming_hook
    slack = slackweb.Slack(url=hook)
    slack.notify(text="{0}({1}): {2}".format(name,nick,message.text))

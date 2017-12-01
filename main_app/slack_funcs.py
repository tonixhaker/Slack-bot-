import slackweb
from slackclient import SlackClient
from .models import Team


def hook_send(message):
    """sends message to selected for bot-hook channel"""
    slack_client = SlackClient(message.team.bot_access_token)
    users = slack_client.api_call("users.list")
    for user in users['members']:
        if user['id'] == message.user_id:
            sender = user
            break
    name = sender['real_name']
    nick = sender['id']

    hook = message.team.incoming_hook
    slack = slackweb.Slack(url=hook)
    slack.notify(text="{0}({1}): {2}".format(name, nick, message.text))


def directmessage(team, id, message):
    """sends direct message to user from bot"""
    token = team.bot_access_token
    slack_client = SlackClient(token)
    users = slack_client.api_call("users.list")
    channel = slack_client.api_call("im.open", user=id)
    channel = channel['channel']['id']
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )


def analyse_thread(event_data):
    """parse message with threads in webhook channel"""
    if 'thread_ts' in event_data['event']:
        thread_ts = event_data['event']['thread_ts']
        channel = event_data['event']['channel']
        team = Team.objects.get(team_id=event_data['team_id'])
        token = team.access_token
        slack_client = SlackClient(token)
        conv = slack_client.api_call(
            "conversations.replies",
            channel=channel,
            ts=thread_ts
        )
        parce_threads(conv, team)


def parce_threads(conv, team):
    main_message = conv['messages'][0]['text']
    index = main_message.index(":")
    main_text = main_message[index + 2:]
    op = main_message.index("(")
    cl = main_message.index(")")
    nickname = main_message[op+1:cl]
    mess_count = len(conv['messages'])-1
    lastanswer = conv['messages'][mess_count]['text']
    directmessage(team, nickname, lastanswer)

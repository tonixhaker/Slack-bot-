from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import slackweb
from slackclient import SlackClient

from .models import Team
from ausers.models import User
import requests
import json


@csrf_exempt
def atpytu(request):
    """command from slack(/atpyti)"""
    print(request.body)
    return HttpResponse("Заявка отправлена!")

@login_required
def slack_oauth(request):
    code = request.GET['code']

    params = {
        'code': code,
        'client_id': settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET
    }
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    Team.objects.get_or_create(
        name=data['team_name'],
        team_id=data['team_id'],
        bot_user_id=data['bot']['bot_user_id'],
        bot_access_token=data['bot']['bot_access_token'],
        incoming_hook=data['incoming_webhook']['url'],
        channelid=data['incoming_webhook']['channel_id'],
        user=request.user
    )
    return redirect('/')


def testsend(request):
    url = "https://hooks.slack.com/services/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"
    slack = slackweb.Slack(url=url)
    slack.notify(text="ЗДАРОВААААА ПЕЕЕС!")
    return redirect('/')


def testdirect(request):
    slack_client = SlackClient('xoxb-279765198183-hQHZ91RLrWDQygeM8bRN0e4O')
    channels_call = slack_client.api_call("users.list")
    print(slack_client.api_call("im.open", user="U86EZ1F99"))
    print(channels_call)
    slack_client.api_call(
        "chat.postMessage",
        channel="D86QGH4HK",
        text="DIRECT MESSAGE HELLO!"
    )
    return redirect('/')
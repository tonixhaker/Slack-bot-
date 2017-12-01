import requests
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from.slack_funcs import hook_send, analyse_thread
from.models import Team, Message


@csrf_exempt
def atpytu(request):
    """command from slack(/atpyti)"""
    try:
        team = Team.objects.get(team_id=request.POST['team_id'])
        user_id = request.POST['user_id']
        text = request.POST['text']
        if len(text) < 10:
            return HttpResponse("Слишком короткое сообщение!")
        message = Message.objects.create(
            team=team,
            user_id=user_id,
            text=text
        )
        hook_send(message)
        return HttpResponse("Заявка отправлена!")
    except:
        return HttpResponse("Ошибка на сервере!")


@login_required
def slack_oauth(request):
    code = request.GET['code']

    params = {
        'code': code,
        'client_id': settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
    }
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    try:
        Team.objects.get(team_id=data['team_id']).delete()
    except:
        print("good")
    Team.objects.get_or_create(
        name=data['team_name'],
        team_id=data['team_id'],
        bot_user_id=data['bot']['bot_user_id'],
        bot_access_token=data['bot']['bot_access_token'],
        incoming_hook=data['incoming_webhook']['url'],
        channelid=data['incoming_webhook']['channel_id'],
        access_token=data['access_token'],
        user=request.user
    )
    return redirect('/')


@csrf_exempt
def event(request):
    print("EVENT")
    try:
        event_data = json.loads(request.body.decode('utf-8'))
        if "challenge" in event_data:
            return HttpResponse(
                event_data.get("challenge")
            )
        analyse_thread(event_data)
        return HttpResponse("ok")
    except:
        return HttpResponse("error")



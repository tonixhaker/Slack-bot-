from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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

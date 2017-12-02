import requests
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.generic import TemplateView

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
            text=text,
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
        team = Team.objects.get(team_id=data['team_id'])
        template = loader.get_template("already-team.html")
        return HttpResponse(template.render())
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


class Dialog(object):

    def __init__(self, parent, answers):
        self.parent = parent
        self.answers = answers

class MessagesDetail(TemplateView):
    template_name = "messages_details.html"

    def get_context_data(self, **kwargs):
        context = super(MessagesDetail, self).get_context_data(**kwargs)
        team = Team.objects.get(id=self.kwargs['pk'])
        context['team'] = team
        messages = team.message_set.all()
        resultarr = []
        for msg in messages:
            answers = msg.answer_set.all()
            resultarr.append(Dialog(msg, answers))
        context['msglist'] = resultarr
        return context


